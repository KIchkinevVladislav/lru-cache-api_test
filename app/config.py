import environ
from dotenv import load_dotenv

load_dotenv()

      
@environ.config(prefix="APP")
class AppConfig:
    capacity_cache: int = environ.var(converter=int, default=10)


app_config: AppConfig = AppConfig.from_environ()
