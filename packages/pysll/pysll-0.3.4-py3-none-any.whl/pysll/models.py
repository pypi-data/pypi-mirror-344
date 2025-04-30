from __future__ import annotations

import base64
import importlib
import inspect
import json
import struct
from dataclasses import dataclass
from typing import BinaryIO, Dict, Iterable, TypedDict, Union

from pysll.decoders import decode

from .exceptions import VariableUnitValueUnparsableExpressionException
from .utils import constellation_date_from_string


@dataclass
class Object:
    id: str
    type: str = ""
    name: str | None = None
    local_path: str = ""

    def __str__(self):
        return self.sll_style_type()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o):
        if self.id != o.id:
            return False
        if self.type != "" and o.type != "":
            return self.type == o.type
        return True

    def sll_style_type(self):
        if self.type:
            type_string_without_object = self.type.replace("Object.", "")
            type_string = ", ".join(type_string_without_object.split("."))
            return f'Object[{type_string}, "{self.id}"]'
        return f'Object["{self.id}"]'


@dataclass
class Model:
    id: str
    type: str | None = None
    name: str | None = None

    def __eq__(self, other):
        return isinstance(other, Model) and (self.id, self.type or other.type) == (other.id, other.type or self.type)

    def sll_style_type(self) -> str:
        if not self.type:
            return f"Model[{self.id}]"

        parts = self.type.split(".")
        head, *types = parts
        if head != "Model":
            types = parts

        return f"Model[{', '.join(types + [self.id])}]"


Kind = Object | Model
ListableKind = Kind | Iterable[Kind]


@dataclass
class BlobRef:
    bucket: str
    path: str
    file_hash: str
    # The local path is set only on BlobRefs that have been downloaded locally
    local_path: str = ""

    def key(self):
        return self.path + self.file_hash

    def __str__(self):
        return "BlobRef[{}, {}, {}]".format(self.bucket, self.path, self.file_hash)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o):
        return self.bucket == o.bucket and self.key() == o.key()

    @classmethod
    def from_dict(cls, data: dict):
        return BlobRef(data["bucket"], data["path"], data["hash"])


class ConstellationFieldDefinition:
    """A structure for holding field definitions from constellation field
    summaries."""

    def __init__(self, count, format, subfields):
        self.count = count
        self.format = format
        self.subfields = subfields

    @classmethod
    def from_dict(cls, data):
        """Create a ConstellationFieldDefinition from a dictionary."""
        return ConstellationFieldDefinition(
            data.get("Count"),
            data.get("Format"),
            [ConstellationSubFieldDefinition.from_dict(subfieldData) for subfieldData in data.get("SubFieldSummaries")],
        )

    def field_info(self, index=-1, name=""):
        """Return the info (e.g., type, units, etc.) for the supplied index and
        name."""
        for subfield in self.subfields:
            if index == -1 or subfield.index == index:
                if name == "" or subfield.name == name:
                    return subfield
        return None


class ConstellationSubFieldDefinition:
    """A structure for holding sub field definitions from constellation field
    summaries."""

    def __init__(self, ecl_type, unit="", name="", index=0):
        self.name = name
        self.index = index
        self.unit = unit
        self.ecl_type = ecl_type

    @classmethod
    def from_dict(cls, data):
        """Create a ConstellationSubFieldDefinition from a dictionary."""
        return ConstellationSubFieldDefinition(
            data.get("Type"),
            data.get("Unit"),
            data.get("Name"),
            data.get("Index"),
        )


class ConstellationFieldParser:
    """Responsible for parsing various constellation field types."""

    def __init__(self, blob_ref_download_api=None):
        self._field_summaries_by_type = {}
        self._cloud_files_encountered = []
        self._blob_refs_encountered = []
        self._blob_ref_download_api = blob_ref_download_api

    def add_summaries_for_type(self, summaries, ecl_type):
        """Add one or more summaries for fields of the supplied types.

        If there is an existing field summary, these will overwrite
        fields that match, but field summaries that are not passed here
        will be untouched in the existing summary store.
        """
        if ecl_type not in self._field_summaries_by_type:
            self._field_summaries_by_type[ecl_type] = {}
        for field_name, field_summary in summaries.items():
            self._field_summaries_by_type[ecl_type][field_name] = ConstellationFieldDefinition.from_dict(field_summary)

    def parse_field_value(self, ecl_type, field_name, field_value, traversal=None):
        """Parse the supplied field value into something that is python
        consumable."""

        # Start with trying to figure out the type from the summaries
        field_info = self._field_info_from_summary(ecl_type, field_name)
        if field_info:
            return self._parse_field_value(field_value, field_info, traversal=traversal)

        # If you couldn't read the summary, check the field value its self
        field_info = self._infer_field_type_from_value(field_value)
        if field_info:
            return self._parse_field_value(field_value, field_info, traversal=traversal)

        # If you couldn't infer it, then just return it unchanged
        return field_value

    def cloud_files_encountered(self):
        """Return a list of the cloud files that were encountered during the
        parsing."""
        return self._cloud_files_encountered

    def _field_info_from_summary(self, ecl_type, field_name):
        """Determine the field type (if possible) from the field summaries."""
        return self._field_summaries_by_type.get(ecl_type, {}).get(field_name)

    def _infer_field_type_from_value(self, field_value: Dict):
        """Try to infer the field type from the value."""
        subfield_values = []
        if isinstance(field_value, list):
            subfield_values = [subfield_value for subfield_value in field_value]
        else:
            subfield_values = [field_value]

        format = "Single"
        if len(subfield_values) > 1:
            # There's no way to infer the difference between a multiple field
            # and a named/indexed single field, so we assume its multiple
            format = "Multiple"

        subfield_definitions = []
        for subfield_value in subfield_values:
            if isinstance(subfield_value, dict):
                supplied_type = field_value.get("$Type")
                if supplied_type:
                    if supplied_type == "__JsonLink__":
                        subfield_definitions.append(ConstellationSubFieldDefinition("Link"))
                        continue
                    if supplied_type == "__JsonBlobReference__":
                        subfield_definitions.append(ConstellationSubFieldDefinition("BlobRef"))
                        continue
            subfield_definitions.append(ConstellationSubFieldDefinition("Unknown"))

        return ConstellationFieldDefinition(len(subfield_values), format, subfield_definitions)

    def _parse_field_value(self, field_value, field_info, map_children=True, traversal=None):
        """Parse the field value correctly based on the info."""
        # If we couldn't figure out the field info, then just return the value unchanged
        if not field_info or len(field_info.subfields) == 0:
            return field_value

        if field_value is None:
            return None

        if traversal and "columns" in traversal:
            if traversal["columns"]["start"] == traversal["columns"]["end"]:
                subfields = [field_info.subfields[traversal["columns"]["start"] - 1]]
            else:
                subfields = field_info.subfields[traversal["columns"]["start"] - 1 : traversal["columns"]["end"] - 1]
        else:
            subfields = field_info.subfields

        # If its a multiple field, then map over it (making sure to not infinitely recurse)
        if field_info.format == "Multiple" and map_children and isinstance(field_value, list):
            return [
                self._parse_field_value(subvalue, field_info, map_children=False, traversal=traversal)
                for subvalue in field_value
            ]

        if len(subfields) == 1:
            # If its a normal single field, then just return it parsed
            return self._parse_subfield(field_value, subfields[0])

        # If we're here, the subfield is named or indexed, so map the subfield values
        # to the subfield definitions
        if isinstance(field_value, list) and len(field_value) == len(subfields):
            results = []
            for subfield_value, subfield_info in zip(field_value, subfields):
                results.append(self._parse_subfield(subfield_value, subfield_info))
            return results

        # If we're here, then we weren't able to get the subfield definitions, so
        # return the value unchanged
        return field_value

    def _parse_subfield(self, field_value, field_info):
        """Parse a subfield value into something consumable by python."""

        # If field_value is None type, return without additional parsing
        if field_value is None:
            return field_value

        # Otherwise, see if we know how to process this type.
        if field_info.ecl_type == "Date":
            return constellation_date_from_string(field_value)
        if field_info.ecl_type == "Float":
            if field_info.unit:
                return VariableUnitValue(field_value, field_info.unit.replace('"', ""))
            return field_value
        if field_info.ecl_type == "String":
            return field_value
        if field_info.ecl_type == "Expression":
            return field_value
        if field_info.ecl_type == "Link":
            obj = self.to_link(field_value)
            if obj.type == "Object.EmeraldCloudFile":
                self._cloud_files_encountered.append(obj)
            return obj
        if field_info.ecl_type == "BlobRef":
            blob_ref = BlobRef.from_dict(field_value)
            self._blob_refs_encountered.append(blob_ref)
            if self._blob_ref_download_api:
                self._blob_ref_download_api(blob_ref)
                if blob_ref.local_path:
                    parsed_result = self.parse_local_file(blob_ref.local_path)
                    if parsed_result:
                        return parsed_result
            return blob_ref
        if field_info.ecl_type == "Byte":
            # If something is a byte field, its very likely to be a quantity array,
            # but not guaranteed. We'll need to investigate how to determine this 100%
            return self.parse_variable_unit_field(field_value)
        if field_info.ecl_type == "VariableUnit":
            return VariableUnitValue.parse_mathematica_expression(field_value.get("mathematica_value", ""))

        # If we don't, then just return the value unchanged
        return field_value

    def to_link(self, field_value):
        """Convert a dictionary field value to a link."""
        obj = field_value["object"]
        id, type = obj["id"], obj.get("type", "")
        klass = Model if type.startswith("Model") else Object
        return klass(id, type)

    def decompress_field(self, data):
        """Decompress the value of a compressed field."""

        return decode(data)

        # The data in a compressed field is first compressed with zlib, then base64 encoded,
        # and the proceeded with a 1. See:
        # https://mathematica.stackexchange.com/questions/104660/what-algorithm-do-the-compress-and-uncompress-functions-use for more info  # noqa: E501

    def parse_variable_unit_field(self, data):
        """Decompress and parse the value of a variable unit field."""
        return VariableUnitValue.parse_mathematica_expression(decode(data))

    def parse_local_file(self, local_path):
        """Attempt to parse a local file into python types.

        If this fails, it will return None
        """
        if not local_path:
            # If local file is not downloaded, it cannot be read
            return None

        # Blob refs are confusing because they are part ascii (specifically
        # a single line header) followed by binary data.  So we do something
        # weird where we read the file as binary and convert the first line
        # into ascii so we can read the header info
        with open(local_path, "rb") as file:
            # NOTE: this is relying on the convention that the header is always on a single line
            # e.g. ending with a newline character. If this ever changes in the blob ref encoding
            # scheme, then we have to edit the code below.
            header_byte_string = file.readline()

            header = header_byte_string.decode("utf-8")

            # convert the header into json
            header_data = json.loads(header)

            # Validate the header is something we can read
            if header_data.get("version") != 1 or header_data.get("encoder") != "binary":
                return None

            # Pull out the unit information, which is just base 64 encoded in the
            # header:
            units = base64.b64decode(header_data.get("mathematicaUnits"))
            parsed_units = VariableUnitValue.parse_mathematica_units_from_expression(units)

            # Parse the values in the file
            results = []
            for row_values in self._parse_binary_value(file, header_data.get("binaryRowFormat")):
                if len(row_values) == 0:
                    continue
                if len(row_values) != len(parsed_units or []):
                    return None
                row_results = []
                for value, unit in zip(row_values, parsed_units or []):
                    row_results.append(VariableUnitValue(value, unit))
                results.append(row_results)

        return results

    def _parse_binary_value(self, filestream, binary_row_format):
        """Parse binary values from a filestream according to the supplied
        binary row format."""

        # Figure out the data width and format based on the binary row format
        # The possible types are stored in the helpfile for ?BinaryRead in mathematica
        # under more options.  Basically, we need to define a map of how many bytes
        # each type is and what the corresponding python value is for each type
        data_width = 0  # size of the row in bytes
        data_format = "<"  # MM is always little endean
        for entry_format in binary_row_format:
            (
                entry_data_width,
                entry_format,
            ) = self._width_and_format_for_mathematica_binary_type(entry_format)
            if entry_format == "" or entry_data_width == 0:
                return None
            data_width += entry_data_width
            data_format += entry_format

        while True:
            data = filestream.read(data_width)
            if len(data) < data_width:
                # end of file
                return
            yield struct.unpack(data_format, data)

    def _width_and_format_for_mathematica_binary_type(self, entry_format):
        """Calculate the width (in bytes) and the correct python type for each
        mathematica type.

        See ?BinaryRead (under details and options) for more info on MM
        types. See
        https://docs.python.org/3/library/struct.html#format-characters
        for more details on python types
        """
        width_and_format_table = {
            "Byte": [1, "b"],
            "Character8": [1, "c"],
            "Character16": [2, ""],
            "Character32": [4, ""],
            "Complex64": [8, ""],
            "Complex128": [16, ""],
            "Complex256": [32, ""],
            "Integer8": [1, "b"],
            "Integer16": [2, "h"],
            "Integer24": [3, ""],
            "Integer32": [4, "i"],
            "Integer64": [8, "q"],
            "Integer128": [16, ""],
            "Real32": [4, "f"],
            "Real64": [8, "d"],
            "Real128": [16, ""],
            "TerminatedString": [0, ""],
            "UnsignedInteger8": [1, "B"],
            "UnsignedInteger16": [2, "H"],
            "UnsignedInteger24": [3, ""],
            "UnsignedInteger32": [4, "I"],
            "UnsignedInteger64": [8, "Q"],
            "UnsignedInteger128": [16, ""],
        }
        width, struct_format = width_and_format_table.get(entry_format, [0, ""])
        return width, struct_format


class VariableUnitValue:
    """Represents a value with a convertable unit (E.g., 1.2 mm)"""

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return str(self.value) + " " + self.unit

    def __eq__(self, o):
        return isinstance(o, VariableUnitValue) and self.value == o.value and self.unit == o.unit

    @classmethod
    def parse_mathematica_expression(cls, mm_expression):
        """Convert the provided MM expression into python structures."""
        return cls._recursively_parse_mm_expression(mm_expression)

    @classmethod
    def parse_mathematica_units_from_expression(cls, mm_expression):
        """Convert a mathematica expression into one or more units."""
        parsed_expression = cls._recursively_parse_mm_expression(mm_expression)
        return cls._parse_mathematica_units_from_parsed_expression(parsed_expression)

    @classmethod
    def _parse_mathematica_units_from_parsed_expression(cls, parsed_expression):
        """Recursively parse mathematica units from a parsed expression."""
        # Once you've hit a string, you have a real unit
        if isinstance(parsed_expression, str):
            return parsed_expression

        # Map over lists, being sure to accomadate "times" units
        if isinstance(parsed_expression, list):
            # Skip empty lists
            if len(parsed_expression) == 0:
                return None
            # Ignore the IndepdentUnit operation:
            if parsed_expression[0] == "IndependentUnit":
                return parsed_expression[1]

            # Perform the times operation
            if parsed_expression[0] == "Times":
                multiplied_unit = ""
                for subunit in parsed_expression[1:]:
                    parsed_subunit = cls._parse_mathematica_units_from_parsed_expression(subunit)
                    if parsed_subunit:
                        if multiplied_unit:
                            multiplied_unit += " "
                        multiplied_unit += parsed_subunit  # type:ignore
                return multiplied_unit

            # For normal lists, just map the result,
            # filtering None results and dropping the list keyword
            if parsed_expression[0] == "List":
                result = []
                for subunit in parsed_expression[1:]:
                    parsed_subunit = cls._parse_mathematica_units_from_parsed_expression(subunit)
                    if parsed_subunit:
                        result.append(parsed_subunit)
                return result

        return None

    @classmethod
    def _recursively_parse_mm_expression(cls, mm_expression):
        """Recursively parse a supplied mm expression into python
        structures."""
        if isinstance(mm_expression, bytes):
            mm_expression = mm_expression.decode("utf-8")

        mm_expression = mm_expression.strip()

        # Check if its the opening of a list
        if mm_expression.startswith("QuantityArray[") and mm_expression.endswith("]"):
            return cls._recursively_parse_mm_expression(mm_expression[14:-1])

        # Check if its the beginning of structured data
        if mm_expression.startswith("StructuredArray`StructuredData[") and mm_expression.endswith("]"):
            return cls._parse_structured_data_expression(mm_expression[31:-1])

        # Check if its the beginning of simple structured array
        if mm_expression.startswith("StructuredArray[") and mm_expression.endswith("]"):
            return cls._parse_structured_array_expression(mm_expression[16:-1])

        # Check if its a quanity
        if mm_expression.startswith("Quantity[") and mm_expression.endswith("]"):
            return cls._parse_quantity_expression(mm_expression[9:-1])

        # Check if its a rule list opening via List[Rule[ keyword
        if mm_expression.startswith("List[Rule[") and mm_expression.endswith("]"):
            return cls._parse_mm_rule_list_expression(mm_expression[5:-1])

        # Check if its a list opening via List keyword
        if mm_expression.startswith("List[") and mm_expression.endswith("]"):
            return cls._parse_mm_list_expression(mm_expression[5:-1])

        # Check if its a list opening via [ character
        if mm_expression.startswith("[") and mm_expression.endswith("]"):
            return cls._parse_mm_list_expression(mm_expression[1:-1])

        # Check if its a list opening via {}
        if mm_expression.startswith("{") and mm_expression.endswith("}"):
            return cls._parse_mm_list_expression(mm_expression[1:-1])

        # Check if its a Rule
        if mm_expression.startswith("Rule[") and mm_expression.endswith("]"):
            return cls._parse_mm_rule_expression(mm_expression[5:-1])

        # Check if its an object
        if mm_expression.startswith("Object[") and mm_expression.endswith("]"):
            return cls._parse_mm_object_expression(mm_expression[7:-1])

        # Check if its a MM null:
        if mm_expression == "Null":
            return None

        # Check if its an int
        try:
            return int(mm_expression.replace("`", ""))
        except ValueError:
            pass

        # Check if its a float
        try:
            return float(mm_expression.replace("`", ""))
        except ValueError:
            pass

        # At this point, its a symbol, so just return it as a string
        # we'll drop the enclosing quotes as they're not needed
        if mm_expression.startswith('"') and mm_expression.endswith('"'):
            mm_expression = mm_expression[1:-1]
        return mm_expression

    @classmethod
    def _parse_mm_list_expression(cls, mm_expression):
        """Parse a list mm expression into a python structure."""
        components = cls._split_by_unenclosed_substring(mm_expression, ",", {"{": "}", "[": "]"})
        return [cls._recursively_parse_mm_expression(component) for component in components]

    @classmethod
    def _parse_mm_rule_expression(cls, mm_expression):
        """Parse a rule mm expression into a python dict."""
        components = cls._split_by_unenclosed_substring(mm_expression, ",", {"{": "}", "[": "]"})
        if len(components) == 2:
            return {
                cls._recursively_parse_mm_expression(components[0]): cls._recursively_parse_mm_expression(  # type:ignore
                    components[1]
                )
            }
        return {}

    @classmethod
    def _parse_mm_rule_list_expression(cls, mm_expression):
        """Parse a rule list mm expression into a python dict."""
        components = cls._split_by_unenclosed_substring(mm_expression, ",", {"{": "}", "[": "]"})
        results = {}
        for component in components:
            result = cls._recursively_parse_mm_expression(component)
            if isinstance(result, dict):
                results.update(result)
        return results

    @classmethod
    def _parse_quantity_expression(cls, mm_expression):
        """Parse a quantity mm expression into a python structure."""
        components = cls._parse_mm_list_expression(mm_expression)
        if len(components) != 2:
            raise VariableUnitValueUnparsableExpressionException("Unexpected quantity components", components)

        return VariableUnitValue(components[0], components[1])

    @classmethod
    def _parse_mm_object_expression(cls, mm_expression):
        """Parse a list mm expression into a python structure."""
        components = cls._split_by_unenclosed_substring(mm_expression.replace(" ", ""), ",", {"{": "}", "[": "]"})
        return Object(id=components[-1], type=".".join(components[:-1]))

    @classmethod
    def _parse_structured_data_expression(cls, mm_expression):
        """Parse a structured data mm expression into a python structure."""
        # The structure data looks like:
        # {Length}, {{val1, ..., valn}, {unit1, ..., unitN}, {additional info}}
        # where each thing can also be a multiple if there's multiple values
        # we don't care about thet length or additional info,
        # so we're just going to pull the values and unit
        structured_data_components = cls._parse_mm_list_expression(mm_expression)

        # there's two forms (at least) that MM can put this in, so let's check each
        if len(structured_data_components) == 2:
            value_list = structured_data_components[1]
            if len(value_list) < 2:  # type:ignore
                raise VariableUnitValueUnparsableExpressionException("Unexpected value list", value_list)

            all_values = value_list[0]  # type:ignore
            all_units = value_list[1]  # type:ignore
        elif len(structured_data_components) > 2:
            all_values = structured_data_components[1]
            all_units = structured_data_components[2]
        else:
            raise VariableUnitValueUnparsableExpressionException(
                "Unexpected structured data components", structured_data_components
            )

        # Sometimes the values are at the top level, and sometimes they're one level
        # down - thanks MM!
        is_multiple = True
        if len(all_values) == 0 or not isinstance(all_values[0], list):  # type:ignore
            all_values = [all_values]
            is_multiple = False

        variable_unit_values = []
        for values in all_values:  # type:ignore
            # Convert the units and values into variable unit objects
            variable_unit_subvalues = []
            for value, unit in zip(values, all_units):  # type:ignore
                variable_unit_subvalues.append(VariableUnitValue(value, unit))
            if is_multiple:
                variable_unit_values.append(variable_unit_subvalues)
            else:
                variable_unit_values = variable_unit_subvalues
        return variable_unit_values

    @classmethod
    def _parse_structured_array_expression(cls, mm_expression):
        """Parse a structured array mm expression into a python structure."""
        components = cls._parse_mm_list_expression(mm_expression)
        if len(components) != 3:
            raise VariableUnitValueUnparsableExpressionException("Unexpected structured array components", components)

        return components[2]

    @classmethod
    def _find_unenclosed_substring(cls, string, substring, enclosing_chars):
        """Find, for example, a comma not contained in {}"""
        open_enclosing_chars = []
        for index in range(len(string)):
            if len(open_enclosing_chars) == 0 and string[index:].startswith(substring):
                return index
            for opening_char, closing_char in enclosing_chars.items():
                if string[index] == opening_char:
                    open_enclosing_chars.append(opening_char)
                if string[index] == closing_char:
                    open_enclosing_chars.remove(opening_char)
        return -1

    @classmethod
    def _split_by_unenclosed_substring(cls, string, substring, enclosing_chars):
        """Split, for example, a comma not contained in {}"""
        results = []
        index = cls._find_unenclosed_substring(string, substring, enclosing_chars)
        while index != -1:
            results.append(string[:index])
            string = string[index + 1 :]
            index = cls._find_unenclosed_substring(string, substring, enclosing_chars)
        results.append(string)
        return results


@dataclass
class CloudFileArgs:
    """Class for arguments that are needed to upload a cloud file to s3 and
    constellation."""

    file: BinaryIO
    name: str
    extension: str
    path: str
    size: int
    key: str
    content_md5: str
    content_disposition: str


class OptionItemDict(TypedDict):
    data_type: str
    name: str
    value: dict


@dataclass
class Option:
    name: str
    value: ListableType


@dataclass
class Quantity:
    value: float
    units: str


@dataclass
class Symbol:
    name: str


@dataclass
class Expression:
    string: str


class Function:
    def __init__(self, *args: ListableType, **kwargs: ListableType):
        self.inputs = list(args)
        self.options = self._build_options_from_kwargs(kwargs)

    def __repr__(self):
        # this isn't final, it just shows that the jupyter nb will render this nicely
        return type(self).__name__ + "[" + str(self.inputs)[:-1] + str(self.options) + "]"

    def _build_options_from_kwargs(self, kwargs: dict) -> list[Option]:
        return [Option(name, val) for name, val in kwargs.items()]

    @staticmethod
    def from_dict(d: dict) -> Function:
        """Method that converts a serialized dictionary into a Function."""
        try:
            assert d["data_type"] == "function"
        except (KeyError, AssertionError):
            raise TypeError("The input dictionary did not have the correct 'data_type' value.")

        try:
            members = {
                kname: klass
                for (kname, klass) in inspect.getmembers(importlib.import_module("pysll.functions"), inspect.isclass)
            }
            unit_op_members = {
                kname: klass
                for (kname, klass) in inspect.getmembers(
                    importlib.import_module("pysll.unit_operations"), inspect.isclass
                )
            }
            members.update(unit_op_members)
            klass = members[d["name"]]
            assert issubclass(klass, Function)
        except (KeyError, AssertionError):
            raise TypeError(
                "Name of the input function is not supported. Either the name has been mispelled or "
                "it is missing from this library."
            )

        return klass(
            *(deserialize_item(inp) for inp in d["inputs"]),
            **{o["name"]: deserialize_item(o["value"]) for o in d["options"]},
        )

    def payload(self) -> FunctionPayload:
        return FunctionPayload(
            data_type="function",
            name=type(self).__name__,
            inputs=serialize_item(self.inputs),
            options=serialize_item(self.options),
        )


@dataclass
class FunctionPayload:
    data_type: str
    name: str
    inputs: ListableDict
    options: ListableDict


@dataclass
class ResultPayload:
    result: ListableDict
    error: bool
    messages: list[str]


SLLItemType = Union[bool, int, float, str, Option, Quantity, Object, Function, Symbol, Expression]
ListableType = SLLItemType | list["ListableType"]
ListableDict = dict | list["ListableDict"]


# NOTE: had to add 'list[Option]' to the input to appease the python type checking gods
# it SHOULD work without it b/c ListableType contains list[Option] by construction
def serialize_item(input: ListableType | list[Option]) -> ListableDict:
    """Convenience function that works for atomic types like int, float, str,
    bool that just converts these to dicts before serializing to json's."""
    match input:
        case list():
            return [serialize_item(inp) for inp in input]
        case bool():
            return {"data_type": "bool", "value": input}
        case int():
            return {"data_type": "integer", "value": input}
        case float():
            return {"data_type": "float", "value": input}
        case str():
            return {"data_type": "string", "value": input}
        case Object(id=id, type=obj_type, name=name):
            return {"data_type": "object", "id": id, "type": obj_type, "name": name}
        # symbol is ultimately a convenience class that gets mapped to an expression on the backend
        case Symbol(name=name):
            return {"data_type": "expression", "string": name}
        case Expression(string=string):
            return {"data_type": "expression", "string": string}
        case Quantity(value=value, units=units):
            return {"data_type": "quantity", "value": value, "units": units}
        case Function(inputs=inputs, options=options):
            if not isinstance(inputs, list):
                raise ValueError("Function contains inputs that are not in a list format, which is prohibited")
            return {
                "data_type": "function",
                "name": type(input).__name__,
                "inputs": [serialize_item(inp) for inp in inputs],
                "options": [serialize_item(op) for op in options],
            }
        case Option(name=name, value=value):
            return {"data_type": "option", "name": name, "value": serialize_item(value)}
        case _:
            raise TypeError(f"The input with type, {type(input)}, cannot be serialized into a dict.")


def deserialize_item(input: ListableDict) -> ListableType:
    """Convenience function that converts a dictionary into a known object
    type."""
    if isinstance(input, list):
        return [deserialize_item(inp) for inp in input]
    data_type = input.get("data_type")
    match input["data_type"]:
        case "integer":
            return int(input["value"])
        case "float":
            return float(input["value"])
        case "string":
            return str(input["value"])
        case "bool":
            return bool(input["value"])
        case "symbol":
            return Symbol(input["name"])
        case "expression":
            return Expression(input["string"])
        case "object":
            return Object(id=input["id"], type=input["type"], name=input["name"])
        case "quantity":
            return Quantity(value=input["value"], units=input["units"])
        case "function":
            return Function.from_dict(input)
        case "option":
            return Option(name=input["name"], value=deserialize_item(input["value"]))
        case _:
            raise TypeError(f"Found a data type that cannot be deserialized: {data_type}")
