def bindCommands(bot):
    
    # TODO: Handle each command as separate module
    
    @bot.command(name='test')
    async def test(ctx):
        await ctx.send('Test response')