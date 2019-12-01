from ..environment import bot_environment

def handle_on_ready(bot):
        print(f'{bot.user.name} has connected to Discord!')
        print('Available on serves: {}'.format(', '.join([server.name for server in bot.guilds])))
        
def handle_on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise