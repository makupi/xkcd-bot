import sys
import traceback

from discord.ext import commands

from utils import Config


class DBLStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = Config.get_dbl_token()

    async def post_count(self):
        headers = {"Authorization": self.token}
        url = f"https://discordbots.org/api/bots/{str(self.bot.user.id)}/stats"
        payload = {"server_count": len(self.bot.guilds)}

        await self.bot.aiohttp.post(url, data=payload, headers=headers)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.post_count()
        except Exception as ex:
            print(f"exception - unloading extension dblstats: {ex}")
            traceback.print_exc(file=sys.stdout)
            self.bot.unload_extension("cogs.dblstats")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.post_count()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.post_count()


def setup(bot):
    bot.add_cog(DBLStats(bot))
