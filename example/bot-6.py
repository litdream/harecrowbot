import os
from dotenv import load_dotenv
from discord.ext import commands

homedir = os.environ['HOME']
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=':')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='version', help="harecrowbot version number" )
async def say_version(ctx):
    await ctx.send('HareCrowBot v0.02')

bot.run(TOKEN)    
