# harecrowbot
This is my personal Discord bot


### venv

```
python3 -m venv venv
source venv/bin/activate

(if missing)
pip install discord.py
  - if dependency fails:  pip install wheel, and inda-ssl
  - another dependency:   pip install python-dotenv requests
  - test dependency:   pip install pytest
  
```

- example uses dotenv (python-dotenv).
  - This dotenv doesn't have to be in the same directory.  I could specify $HOME/.harecrowbot as my app config.  When specifying path, provide filename, also.


### dev
Official Document: https://discordpy.readthedocs.io/en/latest/

TODO:
0. Follow tutorial
  - https://realpython.com/how-to-make-a-discord-bot-python/
1. support /version
2. support /help
3. support /changelog


#### ctx object

ctx can't be pickled because it's weakref object.
discord.py doesn't allow `python -i` either.
guessing introspect by dir():

##### ctx
Link: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context
source: https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/context.py

first line:  type(ctx)
second line:  dir(ctx)
```
<class 'discord.ext.commands.context.Context'>
['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_get_channel', '_state', 'args', 'author', 'bot', 'channel', 'cog', 'command', 'command_failed', 'fetch_message', 'guild', 'history', 'invoke', 'invoked_subcommand', 'invoked_with', 'kwargs', 'me', 'message', 'pins', 'prefix', 'reinvoke', 'send', 'send_help', 'subcommand_passed', 'trigger_typing', 'typing', 'valid', 'view', 'voice_client']

```

##### ctx property types
-- args		: <class 'list'>
-- author	: <class 'discord.member.Member'>
-- bot		: <class 'discord.ext.commands.bot.Bot'>
-- channel	: <class 'discord.channel.TextChannel'>
-- cog		: <class 'NoneType'>
-- command	: <class 'discord.ext.commands.core.Command'>
-- guild	: <class 'discord.guild.Guild'>
-- history	: <class 'method'>
-- me		: <class 'discord.member.Member'>
-- message	: <class 'discord.message.Message'>
-- pins		: <class 'method'>
-- prefix	: <class 'str'>

