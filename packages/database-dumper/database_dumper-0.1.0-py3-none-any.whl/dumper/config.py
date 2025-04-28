import os
import tomllib
from pathlib import Path

from sqlalchemy import URL


TOML_PATH = 'pyproject.toml'


def load_dumper_db_config():
    pyproject_path = Path(TOML_PATH)
    if not pyproject_path.exists():
        return {}

    with pyproject_path.open('rb') as f:
        data = tomllib.load(f)

    tool = data.get('tool', {})
    dumper = tool.get('dumper', {})
    db = dumper.get('db', {})

    return db


class Settings:
    def __init__(self):
        self.toml_data = load_dumper_db_config()
        self.port_prefix = self.toml_data.get('port_prefix', 'PORT')
        self.host_prefix = self.toml_data.get('host_prefix', 'HOST')
        self.user_prefix = self.toml_data.get('user_prefix', 'USER')
        self.pass_prefix = self.toml_data.get('pass_prefix', 'PASS')
        self.database_prefix = self.toml_data.get('database_prefix', 'DB')
        self.env_pattern = self.toml_data.get('env_patten', '{prefix}_{name}')
        self.source_name = self.toml_data.get('source', 'SOURCE')
        self.target_name = self.toml_data.get('target', 'TARGET')

    @property
    def target_url(self) -> str:
        return self.__create_url(self.target_name)

    @property
    def source_url(self) -> str:
        return self.__create_url(self.source_name)

    def set_names(self, source_name: str | None = None, target_name: str | None = None):
        self.source_name = source_name or self.source_name
        self.target_name = target_name or self.target_name

    def __create_url(self, name: str) -> URL:
        return URL.create(
            drivername='postgresql',
            username=os.getenv(self.env_pattern.format(prefix=self.user_prefix, name=name)),
            password=os.getenv(self.env_pattern.format(prefix=self.pass_prefix, name=name)),
            host=os.getenv(self.env_pattern.format(prefix=self.host_prefix, name=name)),
            database=os.getenv(self.env_pattern.format(prefix=self.database_prefix, name=name)),
            port=os.getenv(self.env_pattern.format(prefix=self.port_prefix, name=name)),
        )


settings = Settings()
