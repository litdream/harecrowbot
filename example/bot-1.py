import os

import discord
from dotenv import load_dotenv

homedir=os.environ['HOME']
                   
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)    
