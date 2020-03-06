import random

import aiohttp
import discord
from discord.ext import commands


class Xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            try:
                return await response.json()
            except aiohttp.ContentTypeError:
                return None

    async def get_xkcd(self, _id: int):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, f'http://xkcd.com/{_id}/info.0.json')

    async def get_latest(self):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, f'http://xkcd.com/info.0.json')

    @staticmethod
    def generate_embed(data):
        title = f'xkcd #{data.get("num")} - {data.get("title")}'
        embed = discord.Embed(title=title, url=f'https://xkcd.com/{data.get("num")}')
        embed.set_image(url=data.get('img'))
        return embed

    @commands.command(name='xkcd')
    async def xkcd(self, ctx, number: int):
        data = await self.get_xkcd(number)
        if data is None:
            await ctx.channel.send(f'❌ xkcd #{number} not found. Please try another one.')
            return
        embed = self.generate_embed(data)
        await ctx.channel.send(embed=embed)

    @commands.command(name='latest')
    async def latest_xkcd(self, ctx):
        data = await self.get_latest()
        embed = self.generate_embed(data)
        await ctx.channel.send(embed=embed)

    @commands.command(name='random')
    async def random_xkcd(self, ctx):
        data = await self.get_latest()
        latest_num = data.get('num')
        _id = random.randint(1, latest_num)
        data = await self.get_xkcd(_id)
        embed = self.generate_embed(data)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Xkcd(bot))
