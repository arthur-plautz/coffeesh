import yaml
from models import get_root


class SchemaValidator:
    def __init__(self, exp, method) -> None:
        self.exp = exp
        self.method = method
        self.base_path = f"{get_root()}/{exp}/{method}"
        self.schema_path = self._format_path("data/schema.yml")
        self.schema = self._read(self.schema_path)

    def _validate_list(self, field, value):
        expected = self.schema.get(field)
        if "length" in expected.keys():
            l = expected.get("length")
            if len(value) != l:
               raise Exception(f"Field {field} must have length {l}. Value: {value}")
        if "items_type" in expected.keys():
            t = expected.get("items_type")
            for i in value:
                if isinstance(i, eval(t)):
                    raise Exception(f"Field {field} has incorrect item type [{type(i)}], expected [{t}].")

    def _validate_numeric(self, field, value):
        expected = self.schema.get(field)
        if "range" in expected.keys():
            r = expected.get("range")
            if value < r[0] or value > r[1]:
               raise Exception(f"Field {field} must be in range {r}. Value: {value}")

    def _validate_str(self, field, value):
        expected = self.schema.get(field)
        if "options" in expected.keys():
           o = expected.get("options")
           if value not in o:
               raise Exception(f"Field {field} must be on of {o}. Value: {value}")

    def _validate_field(self, field, value):
        type_validation = {
            "str": self._validate_str,
            "int": self._validate_numeric,
            "float": self._validate_numeric,
            "list": self._validate_list
        }
        expected = self.schema.get(field)
        expected_type = expected.get("type")

        if not isinstance(value, eval(expected_type)):
            raise Exception(f"Field {field} has incorrect type [{type(value)}], expected [{expected_type}].")
        else:
            validation = type_validation.get(expected_type)
            validation(field, value)

    def _format_path(self, path):
        return f"{self.base_path}/{path}"

    def _read(self, path):
        with open(path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def validate(self, path):
        data = self._read(
            self._format_path(path)
        )
        for k, v in data.items():
            self._validate_field(k, v)
