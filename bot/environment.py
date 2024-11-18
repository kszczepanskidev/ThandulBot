from os import getenv, environ
from ast import literal_eval
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    [
        'token',
        'command_channels',
        'role_mentions',
        'weather_token',
        'admin_commands',
        'admin_id',
        'locale',
        'gm_list',
        'foundry_commands',
        'foundry_admins'
    ]
)

bot_environment = Environment(
    environ.get('DISCORD_TOKEN', getenv('DISCORD_TOKEN')),
    literal_eval(environ.get('COMMAND_CHANNELS', getenv('COMMAND_CHANNELS'))),
    literal_eval(environ.get('ROLE_IDS', getenv('ROLE_IDS'))),
    environ.get('WEATHER_TOKEN', getenv('WEATHER_TOKEN')),
    environ.get('ADMIN_COMMANDS', getenv('ADMIN_COMMANDS')),
    environ.get('ADMIN_ID', getenv('ADMIN_ID')),
    environ.get('LOCALE', getenv('LOCALE')),
    literal_eval(environ.get('GM_LIST', getenv('GM_LIST'))),
    environ.get('FOUNDRY_COMMANDS', getenv('FOUNDRY_COMMANDS')),
    literal_eval(environ.get('FOUNDRY_ADMINS', getenv('FOUNDRY_ADMINS'))),
)

emotes = literal_eval(environ.get('EMOTES', getenv('EMOTES')))
