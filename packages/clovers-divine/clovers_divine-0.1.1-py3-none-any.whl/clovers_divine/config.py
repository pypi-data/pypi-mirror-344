from pydantic import BaseModel
from clovers.config import config as clovers_config


class Config(BaseModel):
    daily_fortune_data: str = "data/divine/daily_fortune"
    daily_fortune_resorce: str = "data/divine/daily_fortune/basemap/"
    daily_fortune_title_font: str = "data/divine/daily_fortune/font/Mamelon.otf"
    daily_fortune_text_font: str = "data/divine/daily_fortune/font/sakura.ttf"
    tarot_resource: str = "data/divine/tarot"
    tarot_merge_forward: bool = True


config_key = __package__
config = Config.model_validate(clovers_config.get(config_key, {}))
clovers_config[config_key] = config.model_dump()
