# Now, we will use custom client,
# and custom client will provide event handling.
#
import os

import discord
from dotenv import load_dotenv

homedir=os.environ['HOME']
                   
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_read():
    print(f'{client.user} is connected.')
    
@client.event    
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ':version':
        await message.channel.send('HareCrowBot v0.01')

client.run(TOKEN)
