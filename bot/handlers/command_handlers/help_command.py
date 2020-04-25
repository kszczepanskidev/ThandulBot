def send_help_command(context):
    userId = context.author.id

    with open('..\commands.py', 'r') as f:
        for line in f.readlines():
            if 'bot.command' in line:
                print(line)