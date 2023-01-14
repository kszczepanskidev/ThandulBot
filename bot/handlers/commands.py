from ..environment import bot_environment
from .command_categories.admin_category import AdminCommands
from .command_categories.rpg_category import RPGCommands
from .command_categories.information_category import Information
from .command_categories.animal_photo_category import AnimalRandomPhotos


# Register commands categories.
def bindCommands(commands_tree):
    commands_tree.add_command(AdminCommands(name='admin'))
    commands_tree.add_command(RPGCommands(name='rpg'))
    commands_tree.add_command(Information(name='general'))
    commands_tree.add_command(AnimalRandomPhotos(name='animal'))
