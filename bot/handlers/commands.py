import re
from discord import Embed, Emoji, utils
from ..environment import bot_environment 

emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '0️⃣', ]

def bindCommands(bot):
    
    # TODO: Handle each command as separate module
        
    @bot.command(name='addDates')
    async def addDates(ctx, dates):
        # Check if command was used by allowed user.
        if str(ctx.author.id) != str(bot_environment.admin_id):
            print('Wrong user executed command {} instead of {}'.format(ctx.author.id, bot_environment.admin_id))
            return
        
        dates += ';'
        dates = re.findall(r'(\d{1,2}\.\d{1,2};{1})', dates)
        if len(dates) == 0:
             await ctx.send('No dates found.')
        elif len(dates) > 9:
             await ctx.send('Too many dates found.')
        embed = Embed()
        embed.type = 'rich'
        embed.title = utils.escape_mentions('Terminy na kolejny tydzień. Oznaczcie które dni wam pasują:')
        embed.description = ''
        for it, date in enumerate(dates):
            embed.description += '{}    {}\n\n'.format(emotes[it], date[:-1])
        dates_msg = await ctx.send('<@&{}>'.format(bot_environment.mention_role_id), embed=embed)
        for i in range(0, len(dates)):
            await dates_msg.add_reaction(emotes[i])
        
        
    @bot.command(name='checkDates')
    async def checkDates(ctx):
        channel = ctx.message.channel
        messages = await channel.history(limit=200).flatten()
        print([msg.author for msg in messages])
        last_bot_msg = next(msg for msg in messages if msg.author.name == 'ThandulBot')
        print(last_bot_msg.reactions)