## bot-rpg

`bot-rpg` is a Discord bot designed to help game masters manage their role playing games. It is still in early development, and therefore is not currently available to install on Discord server. Eventually it will be published to some directory of Discord bots for easy installation / invitation.

Each server this bot runs on establishes one *campaign*. Campaigns contain collections of information, such as the current time and date, that relate to a single game. In the future, it will also be possible to put bot-rpg into *multi-campaign* mode. In this instance, there will be one campaign for every distinct channel that the bot is used in. In addition, there will be a private channel for the game master. For example, if the campaign channel is `#abyss`, then the GM channel would be `#abyss-gm` or `#abyss-dm`.

## Limitations

- At the moment, `bot-rpg` has no persistence for campaign information; everything is reset when the bot is restarted. In the future, campaign information will be persisted to a backend server.

- The permissions model is limited. The user who creates the campaign (runs the first slash command after the bot is restarted) becomes the administrator of the campaign, and all other users are "visitors". Most commands may be run as any user.

## Commands

### /set-campaign-time

**Usage:** `/set-campaign-time` `iso-date`

**Required Role:** Game Master

Sets the current date and time in the campaign. When a campaign is first created, the campaign time defaults to noon on June first, 1494, which is a reasonable assumption for a Forgotten Realms campaign.

*Example:* 

```
game-master
/set-campaign-time 1494-06-01 16:30

bot-rpg [bot]
Legacy of Laensburg time: Fri 1494 Jun 01 at 4:30 PM
```

### /pass-time

**Usage:** `/pass-time` `delta`

**Required Role:** Game Master

*Example:* 

```
game-master
/pass-time 2h30m

bot-rpg [bot]
Legacy of Laensburg time: Fri 1494 Jun 01 at 7:00 PM
```

Adds the provided delta to the current time.

### /campaign-time

**Usage:** `/campaign-time`

Prints the current date and time in the campaign.

### /arms

**Usage:** `/arms family-name`

Displays the Coat of Arms for the given family. Autocomplete provides a list of known family names. (I am running a campaign where heraldry and familial relationships are important.)

### /show-arms

**Usage:** `/show-arms family-name message channel`

Works similarly to the `/arms` command, but allows the game master to enter the slash command in a private channel, and display the image in the campaign's general channel. This is useful for showing the arms of a family the party is not yet familiar with.

### /as

**Usage:** `/as role`

Allows a priviledged user to masquerade as a less-priviledged user. Primarily for testing purposes.

## Local Development

```
$ pip install -r requirements.txt
$ python3 -m src.main
```

## Installation

tbd

## Similar Projects

One of the initial ideas for this project was to have a general-purpose RPG bot that would interface with some AI model to help quickly generate campaign information. There are a couple of projects that do something similar, but without an RPG focus. 

- [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot): Integrate ChatGPT, Bing or Bard with your Discord bot.
- [gpt-discord-bot](https://github.com/openai/gpt-discord-bot): Supports conversations with the text-davinci-003 model.
