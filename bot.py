from discord import Game
from discord.ext import commands

from utils import Config

Config.get_token()


def get_prefix(_bot, message):
    return commands.when_mentioned(_bot, message)


bot = commands.AutoShardedBot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.command(name='help')
async def bot_help(ctx):
    await ctx.channel.send(f"""```
@xkcd <id>:     Shows specific comic by id.
@xkcd latest:   Shows latest comic.
@xkcd random:   Shows random comic.
@xkcd help:     Shows this message.```""")


@bot.event
async def on_ready():
    print(f'{bot.user} online.')
    await bot.change_presence(activity=Game(Config.get_game()))


extensions = ['cogs.xkcd', 'cogs.dblstats']
if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(Config.get_token())
