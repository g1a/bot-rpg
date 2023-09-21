import discord
import os
import pathlib

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$arms '):
        name = message.content[6:].title()
        armsPath = '{base}/Arms/{name}.png'.format(base=pathlib.Path(__file__).parent.resolve(), name=name)
        await message.channel.send('name is {name} and arms path is {path}'.format(name=name, path=armsPath))
        await message.channel.send(file=discord.File(armsPath))
    else:
        await message.channel.send('what-do, {author}? You said "{msg}". Your full message object was "{obj}"'.format(author = message.author, msg=message.content, obj=repr(message)))

client.run(os.getenv('TOKEN'))
