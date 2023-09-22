import os
import pathlib

import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #await tree.sync(guild=discord.Object(id='857097491131662346'))
    await tree.sync(guild=discord.Object(id='857097491131662346'))
    print("Ready!")

@tree.command(description="Show Coat of Arms for a player or NPC", guild=discord.Object(id='857097491131662346'))
@app_commands.describe(name='The player or NPC')
async def arms(interaction: discord.Interaction):
    name = interaction.data['options'][0]['value']
    await interaction.response.send_message("Hello!")
    armsPath = '{base}/Arms/{name}.png'.format(base=pathlib.Path(__file__).parent.resolve(), name=name)
    await interaction.response.send_message('name is {name} and arms path is {path}'.format(name=name, path=armsPath))
    await interaction.response.send_message(file=discord.File(armsPath))

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
