import os

import discord
from dotenv import load_dotenv

homedir=os.environ['HOME']
                   
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print(
                f'{client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
            break
        else:
            print(f'skipping guild: {guild.name} (id: {guild.id})')

    members = '\n - '.join( [ member.name for member in guild.members ])
    print(f'Guild Members:\n - {members}')
    
client.run(TOKEN)    
