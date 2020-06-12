import os
from dotenv import load_dotenv
from discord.ext import commands

homedir = os.environ['HOME']
load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
TOKEN = os.getenv('DISCORD_TOKEN')
OWMID = os.getenv('OPENWM_TOKEN')

# Global instances
import bot_mobgame
mobgame = bot_mobgame.Mobgame()

bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='version', help="harecrowbot version number" )
async def say_version(ctx):
    import bot_version
    v = bot_version.Version(ctx)
    await ctx.send(v.version())

@bot.command(name='hello', help='simple hello')
async def say_hello(ctx):
    import bot_hello
    h = bot_hello.Hello(ctx)
    await ctx.send(h.hello())

@bot.command(name="weather", help="weather service")
async def say_hello(ctx, *args):
    import bot_weather
    if len(args) == 0:
        rtn = '''\
USAGE
:weather (zip code | city name) 
'''
    else:
        w = bot_weather.Weather(ctx, OWMID)
        rtn = w.getWeather(*args)
    await ctx.send(rtn)

@bot.command(name="mox", help="mob hunting game")
async def mob_hunt(ctx, *args):
    author = ctx.message.author
    toUser = author.__str__()

    msg = ''
    try:
        if len(args) == 0:
            await ctx.send(mobgame.help())
        else:
            cmd = args[0]
            
            if cmd == 'init':
                msg  = mobgame.setup()
            elif cmd == 'score':
                msg  = mobgame.score()
            elif cmd == 'list':
                msg = mobgame.list()
            else:
                # if not above, it's a hit command with monster
                monster = args[0]
                msg = mobgame.hit(toUser, monster)

    except IndexError:
        msg = "'hit' command require mob-name."
    except Exception as err:
        # TODO: Organize Exception
        msg = err.__str__()

    await ctx.send('{}: {}'.format(toUser, msg))

@bot.command(name="laugh", help="I will laugh")
async def laugh(ctx, *args):
    import bot_laugh
    l = bot_laugh.Laugh(ctx)
    msg = l.laugh()
    await ctx.send(msg)
    
bot.run(TOKEN)    
