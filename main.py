import os
import pathlib

import discord
from discord import option

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="arms", description="Show Coat of Arms for a player or NPC", guild_ids=['857097491131662346'])
@option("name", description="Player or NPC")
async def arms(ctx, name: str):
    armsPath = '{base}/Arms/{name}.png'.format(base=pathlib.Path(__file__).parent.resolve(), name=name)
    await ctx.respond('Arms for {name}:'.format(name=name), file=discord.File(armsPath))

#client.run(os.getenv('TOKEN'))
bot.run(os.getenv('TOKEN'))
