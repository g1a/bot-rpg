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
    name = ctx.guild.name
    # Future: some guilds might want separate campaigns per channel
    # channel=ctx.channel.name, cid=ctx.channel.id
    # When we do this, we'll have to look up the campaign name and
    # not just assume it is the same as the guild name.
    if not key in campaigns:
        campaigns[key] = Campaign(key, name)
    return campaigns[key]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="set-time", description="Set the campaign time")
@option("time", description="Campaign time")
async def set_time(ctx, time: str):
    campaign = get_campaign(ctx)
    campaign.set_time(time)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()), ephemeral=True)

@bot.slash_command(name="campaign-time", description="Display the current campaign time")
async def campaign_time(ctx):
    campaign = get_campaign(ctx)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()))

@bot.slash_command(name="pass-time", description="Advance the campaign time when time passes")
@option("delta", description="How much time has passed")
async def pass_time(ctx, delta: str):
    campaign = get_campaign(ctx)
    campaign.pass_time(delta)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()), ephemeral=True)

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

@bot.slash_command(name="show-arms", description="Display Coat of Arms for a player or NPC in another channel", guild_ids=['857097491131662346'])
@option("name", description="Player or NPC")
@option("message", description="Message to attach above Coat of Arms")
@option("channel", description="Channel to show Coat of Arms")
async def show_arms(ctx, name: str, message: str, channel: str = "general"):
    campaign = get_campaign(ctx)
    arms = campaign.arms()
    if not arms.exists(name):
        await ctx.send_response('No known Coat of Arms for {name}'.format(name=name), ephemeral=True)
        return
    ch = discord.utils.get(bot.get_all_channels(), name=channel)
    if not ch:
        await ctx.send_response('Cannot find a channel named {name}'.format(name=channel), ephemeral=True)
        return
    await ch.send(message, file=discord.File(arms.path(name)))
    await ctx.send_response('Sent arms for {name} to {channel}'.format(name=name, channel=channel))

#client.run(os.getenv('TOKEN'))
if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
