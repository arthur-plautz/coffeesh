import yaml
from models import get_root


class SchemaValidator:
    def __init__(self, exp, method) -> None:
        self.exp = exp
        self.method = method
        self.base_path = f"{get_root()}/{exp}/{method}"
        self.schema_path = self._format_path("data/schema.yml")
        self.schema = self._read(self.schema_path)

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
            expected = self.schema.get(k)
            if not isinstance(v, eval(expected)):
                raise Exception(f"Field {k} has incorrect type [{type(v)}], expected [{expected}].")

