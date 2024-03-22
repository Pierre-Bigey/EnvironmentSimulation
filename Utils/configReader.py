import json

class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.read_config()

    def read_config(self):
        with open(self.file_path, "r") as f:
            config = json.load(f)
        return config

    def get_config(self, *keys):
        """
        Get value(s) from the configuration using one or two keys.
        If one key is provided, returns the corresponding value.
        If two keys are provided, returns the value corresponding to the first key in the nested dictionary
        and the value corresponding to the second key in the nested dictionary.
        """
        if len(keys) == 1:
            return self.config.get(keys[0])
        elif len(keys) == 2:
            first_key = keys[0]
            second_key = keys[1]
            if first_key in self.config:
                nested_dict = self.config[first_key]
                return nested_dict.get(second_key)
        return None

