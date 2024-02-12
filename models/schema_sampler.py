import yaml
import numpy as np
from models.schema_validator import SchemaValidator

class SchemaSampler(SchemaValidator):
    def __init__(self, exp, method):
        self.random_margin = 10
        super().__init__(exp, method)

    def _rand(self):
        return np.random.randint(0, self.random_margin)

    def _generate_field(self, field_type):
        field_types = {
            "str": str(self._rand()),
            "int": int(self._rand()),
            "float": float(self._rand()/(self._rand()+1)),
            "list": [self._rand() for _ in range(self._rand())]
        }
        return field_types.get(field_type)

    def _save(self, data, path):
        with open(path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

    def generate(self, path=None):
        path = path if path else f"data/sample{self._rand()}.yml"

        sample = {}
        for k, v in self.schema.items():
            sample[k] = self._generate_field(v)

        sample_path = self._format_path(path)
        self._save(
            sample,
            sample_path
        )

        print(f"Sample saved [{sample_path}].")
