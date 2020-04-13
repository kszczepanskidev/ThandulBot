from os import getenv, environ
from ast import literal_eval
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    [
        'command_symbol',
        'token',
        'command_channels',
        'mention_role_ids',
        'weather_token',
        'admin_commands',
        'admin_id',
        'bot_id',
        'user_ids',
    ]
)

bot_environment = Environment(
    '!',
    environ.get('DISCORD_TOKEN', getenv('DISCORD_TOKEN')),
    literal_eval(environ.get('COMMAND_CHANNELS', getenv('COMMAND_CHANNELS'))),
    literal_eval(environ.get('ROLE_IDS', getenv('ROLE_IDS'))),
    environ.get('WEATHER_TOKEN', getenv('WEATHER_TOKEN')),
    environ.get('ADMIN_COMMANDS', getenv('ADMIN_COMMANDS')),
    environ.get('ADMIN_ID', getenv('ADMIN_ID')),
    environ.get('BOT_ID', getenv('BOT_ID')),
    literal_eval(environ.get('USER_IDS', getenv('USER_IDS'))),
)

emotes = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', ]