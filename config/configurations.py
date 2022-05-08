from configparser import ConfigParser, NoOptionError, NoSectionError
import os

def load_conf(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        print(e)
        output = default
    return output

def config() -> None:
    config_parse = ConfigParser()
    config_parse.read("settings.ini")
    DATABASE = "DATABASE"
    SYSTEM = "SYSTEM"
    PROXY = "PROXY"

    #DATABASE
    os.environ.setdefault("DATABASE_NAME", load_conf(config_parse, DATABASE, "NAME", "db"))
    os.environ.setdefault("DATABASE_USER", load_conf(config_parse, DATABASE, "USER", "user"))
    os.environ.setdefault("DATABASE_PASSW", load_conf(config_parse, DATABASE, "PASSWORD", "root"))
    os.environ.setdefault("DATABASE_HOST", load_conf(config_parse, DATABASE, "HOST", "localhost"))
    os.environ.setdefault("DATABASE_PORT", load_conf(config_parse, DATABASE, "PORT", "5432"))

    #SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", load_conf(config_parse, SYSTEM, "DEBUG", "False"))
    os.environ.setdefault("DJANGO_KEY", load_conf(config_parse, SYSTEM, "DJANGO_KEY", "root"))
    os.environ.setdefault("ANYCAPTCHA_KEY", load_conf(config_parse, SYSTEM, "ANYCAPTCHA_KEY", None))

    #PROXY
    os.environ.setdefault("PROXY_USERNAME", load_conf(config_parse, PROXY, "PROXY_USERNAME", "root"))
    os.environ.setdefault("PROXY_PASSWORD", load_conf(config_parse, PROXY, "PROXY_PASSWORD", "password"))
    os.environ.setdefault("PROXY_HOST", load_conf(config_parse, PROXY, "PROXY_HOST", "localhost"))
    os.environ.setdefault("PROXY_PORT", load_conf(config_parse, PROXY, "PROXY_PORT", "8000"))