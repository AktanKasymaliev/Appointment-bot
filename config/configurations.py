from configparser import ConfigParser, NoOptionError, NoSectionError
import os
from .settings import env

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

    DATABASE
    os.environ.setdefault("DATABASE_NAME", load_conf(config_parse, DATABASE, "DATABASE_NAME", "botapp"))
    os.environ.setdefault("DATABASE_USER", load_conf(config_parse, DATABASE, "DATABASE_USER", "bot-user"))
    os.environ.setdefault("DATABASE_PASSW", load_conf(config_parse, DATABASE, "DATABASE_PASSWORD", "bots147852"))
    os.environ.setdefault("DATABASE_HOST", load_conf(config_parse, DATABASE, "DATABASE_HOST", "db"))
    os.environ.setdefault("DATABASE_PORT", load_conf(config_parse, DATABASE, "DATABASE_PORT", "5432"))
    # load_conf(config_parse(env('DATABASE_NAME')))
    # load_conf(config_parse(env('DATABASE_USER')))
    # load_conf(config_parse(env('DATABASE_PASSWORD')))
    # load_conf(config_parse(env('DATABASE_HOST')))
    # load_conf(config_parse(env('DATABASE_PORT')))
    # load_conf(config_parse(env('DJANGO_DEBUG')))
    # load_conf(config_parse(env('ANYCAPTCHA_KEY')))
    # load_conf(config_parse(env('DJANGO_KEY')))

    SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", load_conf(config_parse, SYSTEM, "DEBUG", "True"))
    os.environ.setdefault("DJANGO_KEY", load_conf(config_parse, SYSTEM, "DJANGO_KEY", "root"))
    os.environ.setdefault("ANYCAPTCHA_KEY", load_conf(config_parse, SYSTEM, "ANYCAPTCHA_KEY", '41abcc2148244c49816ba8a310a20080'))