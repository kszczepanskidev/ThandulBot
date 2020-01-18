from os import getenv
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
    getenv('DISCORD_TOKEN'),
    literal_eval(getenv('COMMAND_CHANNELS')),
    literal_eval(getenv('ROLE_IDS')),
    getenv('WEATHER_TOKEN'),
    getenv('ADMIN_COMMANDS'),
    getenv('ADMIN_ID'),
    getenv('BOT_ID'),
    literal_eval(getenv('USER_IDS')),
)

emotes = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', ]