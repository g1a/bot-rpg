import os
import pathlib

import discord
from discord import option

from arms import Arms
from campaign import Campaign

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

campaigns = {}

def get_campaign(ctx):
    key = ctx.guild.id
    # Future: some guilds might want separate campaigns per channel
    # channel=ctx.channel.name, cid=ctx.channel.id
    if not key in campaigns:
        campaigns[key] = Campaign(key)
    return campaigns[key]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="arms", description="Show Coat of Arms for a player or NPC", guild_ids=['857097491131662346'])
@option("name", description="Player or NPC")
async def arms(ctx, name: str):
    campaign = get_campaign(ctx)
    arms = campaign.arms()
    if not arms.exists(name):
        await ctx.send_response('No known Coat of Arms for {name}'.format(name=name), ephemeral=True)
        return
    await ctx.send_response(file=discord.File(arms.path(name)))
    await ctx.respond('Guild: {guild} ({id}). Channel: {channel} ({cid}). Arms for {name}:'.format(guild=ctx.guild.name, id=ctx.guild.id, channel=ctx.channel.name, cid=ctx.channel.id, name=name), ephemeral=True)

#client.run(os.getenv('TOKEN'))
bot.run(os.getenv('TOKEN'))
