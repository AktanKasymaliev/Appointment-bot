from configparser import ConfigParser, NoOptionError, NoSectionError

def load_conf(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        output = default
    return output