from configparser import ConfigParser
from pathlib import Path

_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "UI_config.ini"


class Config:
    def __init__(self, config_file=None):
        config_path = Path(config_file) if config_file else _DEFAULT_CONFIG_PATH
        if not config_path.is_file():
            raise FileNotFoundError(f"UI config file not found: {config_path}")
        self.config = ConfigParser()
        read_files = self.config.read(config_path)
        if not read_files:
            raise RuntimeError(f"Failed to load UI config from: {config_path}")

    def _get_required(self, key):
        if key not in self.config['DEFAULT']:
            raise KeyError(f"Missing required key '{key}' in [DEFAULT] section of UI config")
        return self.config['DEFAULT'][key]

    def get_llm_options(self):
        return self._get_required('LLM_OPTIONS').split(', ')

    def get_usecase_options(self):
        return self._get_required('USECASE_OPTIONS').split(', ')

    def get_groq_model_options(self):
        return self._get_required('GROQ_MODEL_OPTIONS').split(', ')

    def get_page_title(self):
        return self._get_required('PAGE_TITLE')

