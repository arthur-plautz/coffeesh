import yaml
import numpy as np
from models.schema_validator import SchemaValidator

class SchemaSampler(SchemaValidator):
    def __init__(self, exp, method):
        super().__init__(exp, method)

    def _generate_value(self, value_type, value_range=(0,10)):
        s, e = value_range
        print(s,e)
        value_types = {
            "str": "-",
            "int": self._rand(s, e),
            "float": sum([0.1 for _ in range(s, self._rand(s, e))]),
        }
        return value_types.get(value_type)

    def _generate_list(self, field):
        expected = self.schema.get(field)
        l = expected.get("length", self._rand())
        t = expected.get("items_type", "str")
        return [self._generate_value(t) for _ in range(l)]

    def _generate_numeric(self, field):
        expected = self.schema.get(field)
        t = expected.get("type")
        r = expected.get("range", (0,10))
        return self._generate_value(t, r)

    def _generate_str(self, field):
        expected = self.schema.get(field)
        o = expected.get("options", [])
        if o:
            return o[self._rand(0, len(o))]
        else:
            return self._generate_value("str")

    def _generate_field(self, field):
        type_generation = {
            "str": self._generate_str,
            "int": self._generate_numeric,
            "float": self._generate_numeric,
            "list": self._generate_list
        }
        expected = self.schema.get(field)
        expected_type = expected.get("type")
        generation = type_generation.get(expected_type)
        return generation(field)

    def _rand(self, min=0, max=10):
        return np.random.randint(min, max)

    def _save(self, data, path):
        with open(path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

    def generate(self, path=None):
        path = path if path else f"data/sample{self._rand()}.yml"

        sample = {}
        for field in self.schema.keys():
            sample[field] = self._generate_field(field)

        sample_path = self._format_path(path)
        self._save(
            sample,
            sample_path
        )

        print(f"Sample saved [{sample_path}].")
