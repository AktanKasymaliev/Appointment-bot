from configparser import ConfigParser, NoOptionError, NoSectionError
import os

def load_conf(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        output = default
    return output

def config() -> None:
    config_parse = ConfigParser()
    config_parse.read("settings.ini")
    DATABASE = "DATABASE"
    SYSTEM = "SYSTEM"

    #DATABASE
    os.environ.setdefault("DATABASE_NAME", load_conf(config_parse, DATABASE, "DATABASE_NAME"))
    os.environ.setdefault("DATABASE_USER", load_conf(config_parse, DATABASE, "DATABASE_USER"))
    os.environ.setdefault("DATABASE_PASSWORD", load_conf(config_parse, DATABASE, "DATABASE_PASSWORD"))
    os.environ.setdefault("DATABASE_HOST", load_conf(config_parse, DATABASE, "DATABASE_HOST"))
    os.environ.setdefault("DATABASE_PORT", load_conf(config_parse, DATABASE, "DATABASE_PORT"))
    
    #SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", load_conf(config_parse, SYSTEM, "DJANGO_DEBUG", "False"))
    os.environ.setdefault("DJANGO_KEY", load_conf(config_parse, SYSTEM, "DJANGO_KEY", "super_secret_key"))
    os.environ.setdefault("ANYCAPTCHA_KEY", load_conf(config_parse, SYSTEM, "ANYCAPTCHA_KEY", None))
