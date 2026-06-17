"""Configuration manager using configparser."""
import os
import configparser

CONFIG_PATH = os.path.join('config', 'settings.ini')

DEFAULT_CONFIG = """
[General]
; general settings

[Logging]
log_file = data/app.log
log_level = INFO

[Updates]
auto_check = true
"""

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        # Create default config
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            f.write(DEFAULT_CONFIG.strip())
    config.read(CONFIG_PATH)
    return config

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        config.write(f)

def get_setting(config, section, option, fallback=None):
    try:
        return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return fallback

def set_setting(config, section, option, value):
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, option, str(value))
    save_config(config)
