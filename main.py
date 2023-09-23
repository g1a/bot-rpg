import os
import pathlib

import discord
from discord import option

from arms import Arms
from campaign import Campaign

campaigns = {}

def get_campaign(guild, channel):
    key = guild.id
    name = guild.name
    # Future: some guilds might want separate campaigns per channel
    #     channel.name, channel.id
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
    campaign = get_campaign(ctx.guild, ctx.channel)
    campaign.set_time(time)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()), ephemeral=True)

@bot.slash_command(name="campaign-time", description="Display the current campaign time")
async def campaign_time(ctx):
    campaign = get_campaign(ctx.guild, ctx.channel)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()))

@bot.slash_command(name="pass-time", description="Advance the campaign time when time passes")
@option("delta", description="How much time has passed")
async def pass_time(ctx, delta: str):
    campaign = get_campaign(ctx.guild, ctx.channel)
    campaign.pass_time(delta)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()), ephemeral=True)

async def get_visible_arms(ctx: discord.AutocompleteContext):
    campaign = get_campaign(ctx.interaction.guild, ctx.interaction.channel)
    arms = campaign.arms()
    return arms.all_visible()

@bot.slash_command(name="arms", description="Show Coat of Arms for a player or NPC", guild_ids=['857097491131662346'])
async def arms(ctx, name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_visible_arms), description="Player or NPC")):
    campaign = get_campaign(ctx.guild, ctx.channel)
    arms = campaign.arms()
    if not arms.exists(name):
        await ctx.send_response('No known Coat of Arms for {name}'.format(name=name), ephemeral=True)
        return
    await ctx.send_response('Arms for {name}:'.format(name=name), file=discord.File(arms.path(name)))

@bot.slash_command(name="show-arms", description="Display Coat of Arms for a player or NPC in another channel", guild_ids=['857097491131662346'])
@option("message", description="Message to attach above Coat of Arms")
@option("channel", description="Channel to show Coat of Arms")
async def show_arms(ctx, name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_visible_arms), description="Player or NPC"), message: str, channel: str = "general"):
    campaign = get_campaign(ctx.guild, ctx.channel)
    arms = campaign.arms()
    if not arms.exists(name):
        await ctx.send_response('No known Coat of Arms for {name}'.format(name=name), ephemeral=True)
        return
    ch = discord.utils.get(bot.get_all_channels(), name=channel)
    if not ch:
        await ctx.send_response('Cannot find a channel named {name}'.format(name=channel), ephemeral=True)
        return
    await ch.send(message, file=discord.File(arms.path(name)))
    await ctx.send_response('Sent arms for {name} to #{channel} channel.'.format(name=name, channel=channel))

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
