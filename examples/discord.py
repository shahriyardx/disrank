import discord
from discord.ext import commands
from disrank.generator import Generator
import functools
import asyncio

class Profile(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_card(self, args):
		image = Generator().generate_profile(**args)
		return image

	@commands.command()
	async def rank(self, ctx, member:discord.Member=None):
		if member is None:
			member = ctx.author
		args = {
			'bg_image' : '', # Background image link (Optional)
			'profile_image' : str(member.avatar_url_as(format='png')), # User profile picture link
			'level' : 1, # User current level 
			'current_xp' : 0, # Current level minimum xp 
			'user_xp' : 10, # User current xp
			'next_xp' : 100, # xp required for next level
			'user_position' : 1, # User position in leaderboard
			'user_name' : str(member), # user name with descriminator 
			'user_status' : member.status.name, # User status eg. online, offline, idle, streaming, dnd
		}

		func = functools.partial(self.get_card, args)
		image = await asyncio.get_event_loop().run_in_executor(None, func)

		file = discord.File(fp=image, filename='image.png')
		await ctx.send(file=file)

def setup(bot):
	bot.add_cog(Profile(bot))