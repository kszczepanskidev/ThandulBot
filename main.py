import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
_token = os.getenv('DISCORD_TOKEN')
_guild = os.getenv('DISCORD_GUILD')
_channels = str(os.getenv('DISCORD_RPG_CHANNELS')).split(';')

bot = commands.Bot(command_prefix='!')


# Inited connection to Discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Handling message errors.
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
        
# Handling new messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.name not in _channels:
        return
    
    print(f'#{message.channel.name}-{message.author.name}: {message.content}')


# Start bot with token
bot.run(_token)