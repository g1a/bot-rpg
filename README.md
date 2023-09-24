## bot-rpg

`bot-rpg` is a Discord bot designed to help game masters manage their role playing games. It is still in early development, and therefore is not currently available to install on Discord server. Eventually it will be published to some directory of Discord bots for easy installation / invitation.

Each server this bot runs on establishes one *campaign*. Campaigns contain collections of information, such as the current time and date, that relate to a single game. In the future, it will also be possible to put bot-rpg into *multi-campaign* mode. In this instance, there will be one campaign for every distinct channel that the bot is used in. In addition, there will be a private channel for the game master. For example, if the campaign channel is `#abyss`, then the GM channel would be `#abyss-gm` or `#abyss-dm`. (Multi-campaign mode is not implemented yet, though.)

## Limitations

- At the moment, `bot-rpg` has no persistence for campaign information; everything is reset when the bot is restarted. In the future, campaign information will be persisted to a backend server.

- The permissions model is limited. The user who creates the campaign (runs the first slash command after the bot is restarted) becomes the administrator of the campaign, and all other users are "visitors". Most commands may be run as any user.

- It's a good idea to establish a campaign by setting the campaign time (or just display the campaign time), as described below. Some autocomplete options do not work well until the campaign has been established.

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

To test locally, you will need to configure your own dev version of bot-rpg. Follow the instructions on the Discord website to [create a new bot](https://discord.com/developers/docs/getting-started). Make note of your application's token.

You might want to skip the "configuration" step, and just use the following invite link:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID_HERE&permissions=380104985664&scope=bot%20applications.commands
```

Then, run your modified copy of bot-rpg on your local machine:

```
$ export TOKEN="Discord bot's secret token"
$ pip install -r requirements.txt
$ python3 -m src.main
```

Note that this project uses the [py-cord library](https://docs.pycord.dev/en/stable/) instead of discord.py. The later is more common, but I found that py-cord worked much better, after struggling a bit too much with discord.py.

## Server Installation

If you fork this repository, you might want to run this bot continuously. For long-term use, a service such as [Sparkedhost](https://sparkedhost.com/discord-bot-hosting) is pretty economical, and probably simplest. (I haven't used Sparkedhost yet, but probably will start using them or some similar service eventually.)

During development, though, you might want to forgo the account creation process, and just run bot-rpg on some systemd-based Linux box. To do so, clone the project on the Linux system, run:

```
$ sudo make install
```

Then you should be able to use systemctl as usual to manage your bot as a service. For example, you should be able to [use systemd to manage your bot's secret token as an environment variable](https://serverfault.com/questions/413397/how-to-set-environment-variable-in-systemd-service). (I haven't set this up yet, so the advice in this section is as of yet untested. I probably will have it running shortly, though.)

## Similar Projects

One of the initial ideas for this project was to have a general-purpose RPG bot that would interface with some AI model to help quickly generate campaign information. There are a couple of projects that do something similar, but without an RPG focus. 

- [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot): Integrate ChatGPT, Bing or Bard with your Discord bot.
- [gpt-discord-bot](https://github.com/openai/gpt-discord-bot): Supports conversations with the text-davinci-003 model.
