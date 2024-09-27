from bot.environment import bot_environment
from bot.bot import bot as ThandulBot

from setproctitle import setproctitle

setproctitle('DiscordBot')

# Start bot with token
ThandulBot.run(bot_environment.token)
