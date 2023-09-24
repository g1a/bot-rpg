import os
import pathlib

import discord
from discord import option

from src.arms import Arms
from src.campaign import Campaign
from src.role_in_campaign import RoleInCampaign

campaigns = {}

def get_campaign(ctx):
    """ Get an existing campaign, or create a new one. """
    key = ctx.guild.id
    name = ctx.guild.name
    creator = ctx.author.id
    # Future: some guilds might want separate campaigns per channel
    #     key = "{guild}:{channel}".format(guild=guild.id, channel=channel.id)
    # When we do this, we'll have to look up the campaign name and
    # not just assume it is the same as the guild name.
    if not key in campaigns:
        campaigns[key] = Campaign(key, name, creator)
    return campaigns[key]

def existing_campaign(guild, channel):
    """ Get the campaign that was already created for the given guild and channel. """
    key = "{guild}:{channel}".format(guild=guild.id, channel=channel.id)
    if key in campaigns:
        return campaigns[key]
    if guild.id in campaigns:
        return campaigns[guild.id]
    return None

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="set-campaign-time", description="Set the campaign time")
@option("time", description="Campaign time")
async def set_campaign_time(ctx, time: str):
    campaign = get_campaign(ctx)
    if not campaign.participants.authorized(ctx.author.id):
        await ctx.send_response('You are not authorized to set the campaign time', ephemeral=True)
        return        
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
    if not campaign.participants.authorized(ctx.author.id):
        await ctx.send_response('You are not authorized to change the campaign time', ephemeral=True)
        return        
    campaign.pass_time(delta)
    await ctx.send_response('{campaign} time: {time}'.format(campaign=campaign.name, time=campaign.time()), ephemeral=True)

async def get_visible_arms(ctx: discord.AutocompleteContext):
    campaign = existing_campaign(ctx.interaction.guild, ctx.interaction.channel)
    if not campaign:
        print('no campaign')
        return []
    arms = campaign.arms()
    return arms.all_visible()

@bot.slash_command(name="arms", description="Show Coat of Arms for a player or NPC")
async def arms(ctx, name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_visible_arms), description="Player or NPC")):
    campaign = get_campaign(ctx)
    arms = campaign.arms()
    if not arms.exists(name):
        await ctx.send_response('No known Coat of Arms for {name}'.format(name=name), ephemeral=True)
        return
    await ctx.send_response('Arms for {name}:'.format(name=name), file=discord.File(arms.path(name)))

@bot.slash_command(name="show-arms", description="Display Coat of Arms for a player or NPC in another channel")
@option("message", description="Message to attach above Coat of Arms")
@option("channel", description="Channel to show Coat of Arms")
async def show_arms(ctx, name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_visible_arms), description="Player or NPC"), message: str, channel: str = "general"):
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
    await ctx.send_response('Sent arms for {name} to #{channel} channel.'.format(name=name, channel=channel))

@bot.slash_command(name="as", description="Act as another role for a time")
@option("role", description="Role to impersonate", choices=RoleInCampaign.all_roles())
#@option("role", description="Role to impersonate", choices=['GAME_MASTER','VISITOR'])
async def set_time(ctx, role: str):
    campaign = get_campaign(ctx)
    acting_role = RoleInCampaign.value_of(role)
    if not campaign.participants.act_as(ctx.author.id, acting_role):
        await ctx.send_response('You are not authorized to act as a {role}'.format(role=role), ephemeral=True)
        return
    await ctx.send_response('Set your acting role to {role}'.format(role=role), ephemeral=True)

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
