from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine, inspect

from .config import settings


load_dotenv()

source_engine = create_engine(settings.source_url)
source_inspector = inspect(source_engine)
source_metadata = MetaData()

target_engine = create_engine(settings.target_url)
target_inspector = inspect(target_engine)
target_metadata = MetaData()
