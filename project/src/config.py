import yaml


def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading config: {e}")
