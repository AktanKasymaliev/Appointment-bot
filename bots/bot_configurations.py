from configparser import ConfigParser, NoOptionError, NoSectionError

def load_conf(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        output = default
    return output

def bot_config_parser_on() -> ConfigParser:
    CONFIG_PARSE = ConfigParser()
    CONFIG_PARSE.read("bot_settings.ini")

    return CONFIG_PARSE

