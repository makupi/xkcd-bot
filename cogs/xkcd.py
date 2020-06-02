import random

import aiohttp
import discord
from discord.ext import commands


class Xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def fetch(session, url):
        response = await session.get(url)
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            return None

    async def get_xkcd(self, _id: int):
        return await self.fetch(self.bot.aiohttp, f"http://xkcd.com/{_id}/info.0.json")

    async def get_latest(self):
        return await self.fetch(self.bot.aiohttp, f"http://xkcd.com/info.0.json")

    @staticmethod
    def generate_embed(data):
        title = f'xkcd #{data.get("num")} - {data.get("title")}'
        embed = discord.Embed(title=title, url=f'https://xkcd.com/{data.get("num")}')
        embed.set_image(url=data.get("img"))
        return embed

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = await self.bot.get_context(message)
        if ctx.valid or message.author.bot:
            return
        if self.bot.user in message.mentions:
            _id = message.content.split()[1]
            try:
                _id = int(_id)
            except ValueError:
                return
            max_xkcd = await self.get_max_xkcd()
            if 1 <= _id <= max_xkcd:
                await self.xkcd(message.channel, _id)
            else:
                await message.channel.send(
                    f"❌ xkcd #{_id} doesn't exist. Please pick between 1-{max_xkcd}."
                )

    async def xkcd(self, channel, number: int):
        data = await self.get_xkcd(number)
        if data is None:
            await channel.send(f"❌ xkcd #{number} not found. Please try another one.")
            return
        embed = self.generate_embed(data)
        await channel.send(embed=embed)

    @commands.command(name="latest")
    async def latest_xkcd(self, ctx):
        data = await self.get_latest()
        embed = self.generate_embed(data)
        await ctx.channel.send(embed=embed)

    @commands.command(name="random")
    async def random_xkcd(self, ctx):
        max_xkcd = await self.get_max_xkcd()
        _id = random.randint(1, max_xkcd)
        data = await self.get_xkcd(_id)
        embed = self.generate_embed(data)
        await ctx.channel.send(embed=embed)

    async def get_max_xkcd(self):
        data = await self.get_latest()
        return data.get("num")


def setup(bot):
    bot.add_cog(Xkcd(bot))
