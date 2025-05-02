from typing import Callable
from pydantic_settings import BaseSettings
import dotenv


dotenv.load_dotenv()


class Config(BaseSettings):
    
    OUTPUT_FILE_DEFAULT_NAME: Callable[[str], str] = lambda desired_format: f"synthex_output.{desired_format}"
    DEBUG_MODE: bool = False
    DEBUG_MODE_FOLDER: str = ".debug"
    
    
config = Config()