from os import getenv
from ast import literal_eval
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    [
        'token',
        'guild',
        'channels',
        'command_symbol',
        'mention_role_ids',
        'admin_id',
        'bot_id',
        'user_ids',
    ]
)

bot_environment = Environment(
    getenv('DISCORD_TOKEN'),
    getenv('DISCORD_GUILD'),
    str(getenv('DISCORD_RPG_CHANNELS')).split(';'),
    '!',
    literal_eval(getenv('DISCORD_ROLE_IDS')),
    getenv('DISCORD_ADMIN_ID'),
    getenv('BOT_ID'),
    literal_eval(getenv('USER_IDS')),
)

emotes = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', ]