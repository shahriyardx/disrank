# Disrank
A lib to make good looking discord profile card

# Usage
```py
from disrank.generator import Generator

args = {
	'bg_image' : '', # Background image link 
	'profile_image' : '', # User profile picture link
	'level' : 1, # User current level 
	'current_xp' : 0, # Current level minimum xp 
	'user_xp' : 10, # User current xp
	'next_xp' : 100, # xp required for next level
	'user_position' : 1, # User position in leaderboard
	'user_name' : 'Name#0001', # user name with descriminator 
	'user_status' : 'online', # User status eg. online, offline, idle, streaming, dnd
}

image = Generator().generate_profile(**args)

# In a discord command
file = discord.File(fp=image, filename='image.png')
await ctx.send(file=file)
```

Make sure to run the generate part in an executor. 
Any help need [Join here](https://discord.gg/7SaE8v2)