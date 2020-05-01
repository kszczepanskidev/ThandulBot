from random import choice
from discord import Embed
from requests import get

apis = {
    'cat': ('https://aws.random.cat/meow', 'file'),
    'dog': ('https://random.dog/woof.json', 'url'),
    'fox': ('https://randomfox.ca/floof/', 'image'),
    'duck': ('https://random-d.uk/api/v2/random', 'url'),
    'goat': 'https://placegoat.com/300',
}

# Fetches URL of random photo of specified animal.
async def post_animal_command(context, animal):
    if animal == 'goat':
        await post_animal_photo(context, apis[animal])
    else:
        response = get(apis[animal][0]).json()
        photoURL = response[apis[animal][1]]
        await post_animal_photo(context, photoURL)

# Fetches URL of random photo of random animal.
async def post_random_animal_command(context):
    animal = choice(list(apis.keys()))
    if animal == 'goat':
        await post_animal_photo(context, apis[animal])
    else:
        response = get(apis[animal][0]).json()
        photoURL = response[apis[animal][1]]
        await post_animal_photo(context, photoURL)

# Posts embed with animal photo and mention of calling user.
async def post_animal_photo(context, photoURL):
    embed = Embed()
    embed.set_image(url=photoURL)
    await context.send(f'<@{context.author.id}>', embed=embed)