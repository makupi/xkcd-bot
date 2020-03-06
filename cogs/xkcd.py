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
            return await response.json()

    async def get_xkcd(self, _id: int):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, f'http://xkcd.com/{_id}/info.0.json')

    async def get_latest(self):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, f'http://xkcd.com/info.0.json')

    def generate_embed(self, data):
        title = f'xkcd #{data.get("num")} - {data.get("title")}'
        embed = discord.Embed(title=title, url=f'https://xkcd.com/{data.get("num")}')
        embed.set_image(url=data.get('img'))
        return embed

    @commands.command(name='xkcd')
    async def xkcd(self, ctx, number: int):
        data = await self.get_xkcd(number)
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
