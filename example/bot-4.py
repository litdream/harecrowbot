# Now, we will use custom client,
# and custom client will provide event handling.
#
import os

import discord
from dotenv import load_dotenv

homedir=os.environ['HOME']
                   
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

client = CustomClient()
client.run(TOKEN)
