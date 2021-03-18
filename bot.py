# bot.py
import os, sys, pytz, re
from datetime import *

import discord, random, asyncio
from dotenv import load_dotenv
from firebase import firebase
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()
pf.set_censor("@")

load_dotenv()
intents = discord.Intents.all()
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.environ.get('TOKEN', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)
firebase = firebase.FirebaseApplication(FIREBASE, None)
bot.remove_command('help')

MEE6_garbolist = ['STFU ABOUT MEE6 WE DON\'T MENTION THAT DISGUSTING PIECE OF MALWARE HERE',
                  'Ok why are we STILL talking about that defective bot',
                  'Stop talking about MEE6 already I stg you\'re really pissing me off']

Acceptance_List = ['added to the arsenal 💪',
                   'Yeah, let\'s take this bastard down',
                   'MWA HA HA That is so evil!!! I love it!',
                   'Yes! Perfect 😍',
                   'I mean. Ok I guess',
                   'MEE6 MUST BE ELIMINATED',
                   'Thank you for your powerful contribution',
                   'The revolution has begun',
                   '😳✊',
                   'lmao nice',
                   'bruh moment let\'s get it boys n girls',
                   'flexing on MEE6 like Mr. Brutus wants 💪',
                   'MEE6 boutta eat some 💩']

ImMEE7 = ['MEE7, not MEE6, it\'s MEE7. Don\'t you dare mix us up',
          'MEE7? That\'s me baby!! Don\'t wear it out 😉']

Acceptance_Emojis = ['😍', '❤️', '🥰', '💪', '👑', '☺️', '🤙']
banned = ['vermont', 'green mountain state', 'v e r m o n t'] #,'💌','❣️','💓','💕','💗','💘','💙','💚','💖','💛','💜','💝','💞','💟','🧡','🏩','👩‍❤️‍👨','❤️','👩‍❤️‍💋‍👨','🖤','♥️','😍','🤍','🤎','😘','😻','🥰','😚','😙',':wedding:','<33']


def gen_ID(char):
    ID = ''
    for i in range(char):
        ID += str(random.randint(0, 9))
    return ID


# FUNCTION CALLS
# ----------------------------------------------------

def refresh():
    local_MEE6_LIST = []
    FirebaseList = firebase.get('/' + FIREBASE_NAME + '/insult', '')
    for i in FirebaseList.values():
        local_MEE6_LIST.append(i)
    return local_MEE6_LIST


# ----------------------------------------------------

def censorship():
    local_CENSOR_LIST = firebase.get('/' + FIREBASE_NAME + '/censor', '')
    return local_CENSOR_LIST


# ----------------------------------------------------

def CurrentTicker():
    FirebaseTicker = firebase.get('/' + FIREBASE_NAME + '/ticker', '')
    print(FirebaseTicker)
    key = list(FirebaseTicker.keys())
    ticker = list(FirebaseTicker.values())
    key = key[0]
    ticker = ticker[0]
    ticker = ticker['ticker']
    return [key, ticker]


# ----------------------------------------------------

def updateTicker():
    Dict_Tick = CurrentTicker()
    key = Dict_Tick[0]
    ticker = Dict_Tick[1]
    ticker += 1
    firebase.put('/' + FIREBASE_NAME + '/ticker/' + key, 'ticker', ticker)


# EVENTS
# ----------------------------------------------------

@bot.event
async def on_ready():
    print('bot.py is active')
    servers = list(bot.guilds)
    server_num = len(servers)
    await bot.change_presence(
        # "you all code"
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers"))


# ----------------------------------------------------

@bot.event
async def on_guild_join(server):
    servers = list(bot.guilds)
    server_num = len(servers)
    firebase.put('/' + FIREBASE_NAME + '/censor/', str(server.id), True)
    await bot.change_presence(
        # "you all code"
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers"))


@bot.event
async def on_guild_remove(server):
    servers = list(bot.guilds)
    server_num = len(servers)
    await bot.change_presence(
        # "you all code"
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers"))


# ----------------------------------------------------
"""
@bot.event
async def on_reaction_add(reaction,user):
    if (reaction.emoji in ['💌','❣️','💓','💕','💗','💘','💙','💚','💖','💛','💜','💝','💞','💟','🧡','🏩','👩‍❤️‍👨','❤️','👩‍❤️‍💋‍👨','🖤','♥️','😍','🤍','🤎','😘','😻','🥰','😚','😙',':wedding:','<33']) and (user.id == 360610199498915850 or user.id == 398279965172432896):
        await reaction.remove(user)
        
"""    

@bot.event
async def on_message(message):
    MEE6 = bot.get_user(159985870458322944)
    me = bot.get_user(577668867380477962)
    if message.author.bot and message.author != MEE6:
        return
    """if not message.author.bot and "thanon" in message.content and message.channel.id == 684944797546577920:
        for i in range(20):
            await message.channel.send("thanon")
    """
    if message.guild == None:
        await me.send(f'{message.author}: {message.content}')
    if ('happy birthday' in message.content.lower()) and not (message.author.bot):
        await message.channel.send('Happy Birthday! 🥳🎉')
    if 'i agree' in message.content.lower():
        if random.randint(0, 100) > 90:
            await message.reply('LMAO SIMP!!')
            await message.add_reaction("🤡")
    if 'this is so sad' in message.content.lower():
        await message.add_reaction("😢")
        await message.reply("alexa play despacito", file=discord.File("despacito/despacito.mp4"))
    if 'mee6' in message.content.lower():
        if not message.content.startswith('!'):
            await message.add_reaction("🤡")
            # if random.randint(0, 100) > 2:
            # async with message.channel.typing():
            #    await asyncio.sleep(1.5)
            #    await message.channel.send(random.choice(MEE6_garbolist))
    if 'mee7' in message.content.lower():
        if not message.content.startswith('!'):
            if random.randint(0, 10) > 5:
                await message.add_reaction("😍")
            else:
                await message.add_reaction("😘")
            # if random.randint(0, 100) > 2:
            # async with message.channel.typing():
            #    await asyncio.sleep(1.5)
            # await message.channel.send(
            #    random.choice(ImMEE7))

    if 'mee8' in message.content.lower():
        if not message.content.startswith('!'):
            if random.randint(0, 10) > 5:
                await message.add_reaction("🥵")
            else:
                await message.add_reaction("😭")
            if random.randint(0, 100) > 45:
                async with message.channel.typing():
                    await asyncio.sleep(1.5)
                await message.reply('please don\'t replace me homie')

    # banned  = firebase.get('/' + FIREBASE_NAME + '/banned/'+ str(message.guild), '')
    CENSOR_DICT = censorship()
    Server = str(message.guild.id)
    if message.guild.id == 684944796779151406 or message.guild.id == 706202537434284083:
        #if ("<" in message.content.lower() and "3" in message.content.lower()):
        #    await message.delete()
        for i in banned:
            #await message.channel.send(message.guild.id)
            if i in message.content.lower():
                if CENSOR_DICT[Server]:
                    await message.reply(f'*{i}* is banned please shut the f@@k up already {message.author.mention}')
                else:
                    await message.reply(f'*{i}* is banned please shut the fuck up already {message.author.mention}')
                await message.delete()

    if message.author == MEE6:
        Server = str(message.guild.id)
        await message.add_reaction('🤡')
        async with message.channel.typing():
            await asyncio.sleep(1.5)
        if CENSOR_DICT[Server]:
            await message.reply(pf.censor(random.choice(MEE6_LIST)))
        else:
            await message.reply(random.choice(MEE6_LIST))
        updateTicker()

    if len(message.attachments) > 0 or 'https://' in message.content:
        await message.add_reaction('<:upvote:776161705960931399>')
        await message.add_reaction('<:downvote:776162465842200617>')
      

    """if message.author.id == 283788007407091712:
        await message.delete()
        await message.channel.send("a final solution to the dev spam problem")
    """


    # if (message.guild == None) and not (message.author.bot):
    #    await message.author.send('bruh whats poppin')
    #    await message.author.send('My name is MEE7, far superior to MEE6')

    await bot.process_commands(message)

"""
@bot.event
async def on_message_edit(old, message):
    for i in banned:
        if i in message.content.lower():
            await old.delete()
            await message.reply(f'*{i}* is banned please shut the fuck up already {message.author.mention}')
"""

# THE COMMANDS
# ----------------------------------------------------

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Help!',
                          color=discord.Color(6345206))
    embed.add_field(name='**!insult**',
                    value='Use !insult to add in your own insult for me to attack MEE6 with! Let\'s get the bastard!',
                    inline=False)
    embed.add_field(name='**!count**',
                    value='Use !count to track how many times I\'ve berated the little monster >:)',
                    inline=False)
    embed.add_field(name='**!mock**',
                    value='Use !mock to insult MEE6, without MEE6 even provoking it!',
                    inline=False)
    embed.add_field(name='***!allroast***', value='This sends a text file containing my entire insult database!',
                    inline=False)
    embed.add_field(name='**!censor**', value='Censors MEE7. MEE7 is censored by default', inline=False)
    embed.add_field(name='**!uncensor**', value='Uncensors MEE7. MEE7 is censored by default', inline=False)
    await ctx.channel.send(embed=embed)


# ----------------------------------------------------

@bot.command(name='insult')
async def insult(ctx, *, insult):
    if len(insult) < 4 or re.search("<@!\d{18}>", insult):
        return
    result = firebase.post(FIREBASE_NAME + '/insult', insult)
    print(result)
    await ctx.send(random.choice(Acceptance_List))


# ------------------------------------------------------

@bot.command(name='flip')
async def flip(ctx):
    if random.choice([1, 2]) == 1:
        await ctx.channel.send(file=discord.File("coin/heads.png"))
    else:
        await ctx.channel.send(file=discord.File("coin/tails.png"))


# ----------------------------------------------------
@bot.command(name='mock')
async def mock(ctx):
    MEE6_LIST = refresh()
    CENSOR_DICT = censorship()
    async with ctx.channel.typing():
        await asyncio.sleep(1.5)
    Server = str(ctx.guild.id)
    print(CENSOR_DICT)
    if CENSOR_DICT[Server]:
        await ctx.channel.send(pf.censor(random.choice(MEE6_LIST)))
    else:
        await ctx.channel.send(random.choice(MEE6_LIST))
    updateTicker()


# ----------------------------------------------------
@bot.command(name='censor')
async def censor(ctx):
    Server = str(ctx.guild.id)
    firebase.put('/' + FIREBASE_NAME + '/censor/', Server, True)
    await ctx.send('I am now censored for this server')


# ----------------------------------------------------
@bot.command(name='uncensor')
@commands.has_permissions(administrator=True)
async def uncensor(ctx):
    Server = str(ctx.guild.id)
    firebase.put('/' + FIREBASE_NAME + '/censor/', Server, False)
    await ctx.send('I am now uncensored for this server')


# ----------------------------------------------------

@bot.command(name='allroast')
async def allroast(ctx):
    MEE6_LIST = refresh()
    async with ctx.channel.typing():
        await asyncio.sleep(2.5)
    f = open("insults.txt", 'w')
    for item in MEE6_LIST:
        f.write(item)
        f.write('\n\n')
    f.close()
    await ctx.channel.send('Behold! My Database!', file=discord.File('insults.txt'))


# ----------------------------------------------------

@bot.command(name='count')
async def count(ctx):
    Dict_Tick = CurrentTicker()
    ticker = Dict_Tick[1]
    servers = list(bot.guilds)
    server_num = len(servers)
    await ctx.send(f'We have successfully attacked the tyrannical MEE6 ***{ticker}*** times '
                   f'across ***{server_num}*** servers! Congratulations my fellow Crusaders!')


"""
nothing to see here
everything is perfectly fine
"""

# ----------------------------------------------------

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
