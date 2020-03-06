import discord
from discord import Game
from discord.ext import commands

from utils import Config

Config.get_token()


def get_prefix(_bot, message):
    prefix = _bot.prefix
    return commands.when_mentioned_or(prefix)(_bot, message)


bot = commands.AutoShardedBot(command_prefix=get_prefix)
bot.prefix = Config.get_prefix()


@bot.event
async def on_ready():
    print(f'{bot.user} online.')
    await bot.change_presence(activity=Game(Config.get_game()))


extensions = ['cogs.xkcd']
if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(Config.get_token())
