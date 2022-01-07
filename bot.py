# bot.py
import os, sys, pytz, re
from datetime import *

import discord, random, asyncio,json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from profanityfilter import ProfanityFilter
from cogs.fun import attachm
pf = ProfanityFilter()
pf.set_censor("@")

import colorama
from colorama import Fore
from colorama import Style

load_dotenv()
intents = discord.Intents.all()
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='?', intents=intents)
TOKEN = os.environ.get('TOKEN', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)

cred = credentials.Certificate("mee7fbkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE
})
all_data = db.reference('/')

#firebase = firebase.FirebaseApplication(FIREBASE, None)
bot.remove_command('help')
# TODO: charades game

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

"""
def download_firebase():
    firebase_database = firebase.get('/' + FIREBASE_NAME, '')
    #print(firebase_database)
    with open('data.json', 'w') as outfile:
        json.dump(firebase_database, outfile, indent=4,sort_keys=True)
"""

def refresh():
    local_MEE6_LIST = []
    #FirebaseList = firebase.get('/' + FIREBASE_NAME + '/insult', '')
    FirebaseList = all_data.child('insult').get()
    for i in FirebaseList.values():
        local_MEE6_LIST.append(i)
    return local_MEE6_LIST


# ----------------------------------------------------

def censorship():
    #local_CENSOR_LIST = firebase.get('/' + FIREBASE_NAME + '/censor', '')
    local_CENSOR_LIST = all_data.child('censor').get()
    return local_CENSOR_LIST


# ----------------------------------------------------

def CurrentTicker():
    #FirebaseTicker = firebase.get('/' + FIREBASE_NAME + '/ticker', '')
    FirebaseTicker = all_data.child('ticker').get()
    return FirebaseTicker


# ----------------------------------------------------

def updateTicker():
    ticker = CurrentTicker()
    ticker += 1
    all_data.child('ticker').set(ticker)
    #firebase.put('/' + FIREBASE_NAME + '/ticker/' + key, 'ticker', ticker)
    
# EVENTS
# ----------------------------------------------------

@bot.event
async def on_ready():
    print(Fore.GREEN + Style.BRIGHT + 'bot.py is active' + Style.RESET_ALL)
    servers = list(bot.guilds)
    server_num = len(servers)
    await bot.change_presence(
        # "you all code"
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers"))
        #activity=discord.Activity(type=discord.ActivityType.watching, name=f"USE ? FOR COMMANDS NOW"))


# ----------------------------------------------------

@bot.event
async def on_guild_join(server):
    servers = list(bot.guilds)
    server_num = len(servers)
    all_data.child('censor').child(str(server.id)).update(True)
    #firebase.put('/' + FIREBASE_NAME + '/censor/', str(server.id), True)
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


# PAYLOAD REACTION --> BASED AND UPVOTE TRACKER
# ----------------------------------------------------
@bot.event
async def on_raw_reaction_add(payload):
    # NOTE: We have to use the raw function because on the regular reaction, it
    #       only does it for cached messages, which is not ideal
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    message_ = await channel.fetch_message(payload.message_id)
    me = bot.get_user(577668867380477962)
    mee7 = bot.get_user(706194661366300753)

    downvote = bot.get_emoji(776162465842200617) # '<:downvote:776162465842200617>'
    upvote = bot.get_emoji(776161705960931399)
    based = bot.get_emoji(764140006640975922)
    if user != message_.author:
        if payload.emoji == upvote:
            try:
                message_firebase = all_data.child('upvotecount')
                id_dict = message_firebase.get()
                upCount = id_dict[str(message_.author.id)]
                newUpCount = int(upCount) + 1
                UpUpdateCount = message_firebase.update({str(message_.author.id):newUpCount})
            except Exception as e:
                print(e)
                upStartCount = all_data.child('upvotecount').update({str(message_.author.id): 1})
                
        if payload.emoji == downvote:
            if message_.author == me and user != mee7:
                await message_.remove_reaction(downvote, user)
                return
            try:
                await asyncio.sleep(0.5)
                message_firebase = all_data.child('upvotecount')
                id_dict = message_firebase.get()
                upCount = id_dict[str(message_.author.id)]
                newUpCount = int(upCount) - 1
                UpUpdateCount = message_firebase.update({str(message_.author.id): newUpCount})
                #await reaction.message.channel.send(f'upvote count {newUpCount}')
            except Exception as e:
                print(e)
                upStartCount = all_data.child('upvotecount').update({str(message_.author.id): -1})
                
        if payload.emoji == based:
            try:
                #basedCount = firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(message_.author.id), '')
                message_firebase = all_data.child('basedcount')
                id_dict = message_firebase.get()
                basedCount = id_dict[str(message_.author.id)]
                newBasedCount = int(basedCount) + 1
                basedUpdateCount = message_firebase.update({str(message_.author.id): newBasedCount})
                #await ctx.send(f'based count {newBasedCount}')
            except:
                basedStartCount = all_data.child('basedcount').update({str(message_.author.id): 1})

# ON MESSAGE BRO
# ----------------------------------------------------

@bot.event
async def on_message(message):
    MEE6 = bot.get_user(159985870458322944)
    me = bot.get_user(577668867380477962)
    if message.author.bot and message.author != MEE6:
        return
    if ('happy birthday' in message.content.lower()) and not (message.author.bot):
        await message.channel.send('Happy Birthday! 🥳🎉')
    if 'i agree' in message.content.lower():
        if random.randint(0, 100) > 90:
            await message.reply('LMAO SIMP!!')
            await message.add_reaction("🤡")
    if 'this is so sad' in message.content.lower():
        await message.add_reaction("😢")
        await message.reply("alexa play despacito\n\n\nhttps://cdn.discordapp.com/attachments/840745532736667648/840746309727158333/despacito.mp4")
    if 'praise mark' in message.content.lower():
        await message.add_reaction('<:mark:827299997602545704>')
        praisemark = await message.reply("praise mark\n\n\nhttps://cdn.discordapp.com/attachments/840745532736667648/840746314752196678/mark.mp4")
        await praisemark.add_reaction('<:mark:827299997602545704>')
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
        MEE6_LIST=refresh()
        await message.add_reaction('🤡')
        async with message.channel.typing():
            await asyncio.sleep(1.5)
        if CENSOR_DICT[Server]:
            await message.reply(pf.censor(random.choice(MEE6_LIST)))
        else:
            await message.reply(random.choice(MEE6_LIST))
        updateTicker()

    if attachm(message):
        try:
            await message.add_reaction('<:upvote:776161705960931399>')
            await message.add_reaction('<:downvote:776162465842200617>')
        except Exception as e:
            # no permissions to execute this reaction 
            print("put in permission error pass here so no cluttered logs")
      
    """if message.author.id == 283788007407091712:
        await message.delete()
        await message.channel.send("a solution to the dev spam problem")
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

# embeds
# ----------------------------------------------
def embedNone():
        embed = discord.Embed(title='Help: Categories!', description="Type ?help {category} for commands in a specific category",
                          color=discord.Color(6345206))
        embed.add_field(name='**MEE6**',
                    value='MEE6 related commands',
                    inline=False)
        embed.add_field(name='**Admin**',
                    value='Administrative commands',
                    inline=False)
        embed.add_field(name='**Barter System**',
                    value='Barter System commands _in current development_',
                    inline=False)
        embed.add_field(name='**Media**',
                    value='Video, GIF, and Image commands',
                    inline=False)
        embed.add_field(name='**Misc**',
                    value='Miscellaneous commands',
                    inline=False)
        return embed
def embedMee6():
    embed = discord.Embed(title='Help: MEE6', description="MEE7's anti-Mee6 commands",
                        color=discord.Color(6345206))
    embed.add_field(name='**insult**',
                    value='Use !insult to add in your own insult for me to attack MEE6 with! Let\'s get the bastard!',
                    inline=False)
    embed.add_field(name='**count**',
                    value='Use !count to track how many times I\'ve berated the little monster >:)',
                    inline=False)
    embed.add_field(name='**!mock**',
                    value='Use !mock to insult MEE6, without MEE6 even provoking it!',
                    inline=False)
    embed.add_field(name='***allroast***', value='This sends a text file containing my entire insult database!',
                    inline=False)
    embed.add_field(name='**censor**', value='Censors MEE7. MEE7 is censored by default', inline=False)
    embed.add_field(name='**uncensor**', value='Uncensors MEE7. MEE7 is censored by default', inline=False)
    return embed   
def embedAdmin():
    embed = discord.Embed(title='Help: Admin', description="MEE7's list of administrative commands",
                        color=discord.Color(6345206))
    embed.add_field(name='**kick _{@person_}**',
                    value='Kicks people',
                    inline=False)
    embed.add_field(name='**ban _{@person}_**',
                    value='Bans people',
                    inline=False)
    embed.add_field(name='**clear _{number}_**',
                    value='Deletes _{number}_ of messages in channel',
                    inline=False)
    embed.add_field(name='***unban _{user ID}_***', 
                    value='in development',
                    inline=False)
    embed.add_field(name='**invite _{user ID}_**', 
                    value='in development', 
                    inline=False)
    return embed
def embedBarter():
    embed = discord.Embed(title='Help: Barter', description="MEE7 tracks all of your baseds and upvotes across every server that it is on. reply to someone with 'based' to increase their count, and react with the based and upvote reactions",
                        color=discord.Color(6345206))
    embed.add_field(name='**upvote**',
                    value='Sends leaderboard of all upvotes',
                    inline=False)
    embed.add_field(name='**based**',
                    value='Sends leaderboard of all baseds',
                    inline=False)
    embed.add_field(name='**giveb _{@person}_ _{number}_**',
                    value='Gives _{@person}_ _{number}_ more upvotes',
                    inline=False)
    embed.add_field(name='***giveb _{@person}_ _{number}_***', 
                    value='Gives _{@person}_ _{number}_ more baseds',
                    inline=False)
    embed.add_field(name='**MORE COMING SOON!**', 
                    value='in development', 
                    inline=False)
    return embed
def embedMedia():
    embed = discord.Embed(title='Help: Media', description="MEE7 allows you to perform several operations on a user's provided media \n_**Works for replies**_ means you can reply to a message with an attachment/link and it will still work",
                        color=discord.Color(6345206))
    embed.add_field(name='**caption _{attachment}_**',
                    value='Captions media. Works for replies',
                    inline=False)
    embed.add_field(name='**deepfry _{number} {attachment}_**',
                    value='deepfries media _{number}_ times. Works for replies',
                    inline=False)
    embed.add_field(name='**download _{link}_**',
                    value='Downloads a video from a link (reddit/youtube/etc). Works for replies',
                    inline=False)
    embed.add_field(name='**speed _{link/attachment}_**', 
                    value='Increases or Decreases the speed of a video. Works for replies',
                    inline=False)
    embed.add_field(name='**convert _{link/attachment}_**', 
                    value='Converts a video/link to an MP4 attachment. Works for replies',
                    inline=False)
    embed.add_field(name='**MORE COMING SOON!**', 
                    value='in development', 
                    inline=False)
    return embed
def embedMisc():
    embed = discord.Embed(title='Help: Misc', description="MEE7 Miscellaneous commands",
                        color=discord.Color(6345206))
    embed.add_field(name='**flip**',
                    value='Flips a coin',
                    inline=False)
    embed.add_field(name='**info _{@person}_**',
                    value='Sends _{@person}_\'s account info IN DEVELOPMENT',
                    inline=False)
    embed.add_field(name='**av _{@person}_**',
                    value='Sends _{@person}_\'s avatar',
                    inline=False)
    return embed
def embedWhat():
    embed = discord.Embed(title='Bro what??', description="I have no idea what that category is my guy",
                color=discord.Color(6345206))
    return embed

# THE COMMANDS
# ----------------------------------------------------

@bot.command(name='help')
async def help(ctx, cate=None):
    await ctx.message.add_reaction("✅")
    help_switch = {
        None: embedNone(),
        "mee6": embedMee6(),
        "admin": embedAdmin(),
        "barter": embedBarter(),
        "media": embedMedia(),
        "misc": embedMisc(),
        "?": embedWhat()
    }
    if cate is not None:
        cate = cate.lower()
    try:
        embed = help_switch[cate]
    except:
        embed = help_switch["?"]
    await ctx.channel.send(embed=embed)


# ----------------------------------------------------

@bot.command(name='insult')
async def insult(ctx, *, insult):
    await ctx.message.add_reaction("✅")
    if len(insult) < 4 or re.search("<@!\d{18}>", insult):
        return
    result = all_data.child('insult').update({insult: insult})
    print(result)
    await ctx.send(random.choice(Acceptance_List))

# ----------------------------------------------------
@bot.command(name='mock')
async def mock(ctx):
    await ctx.message.add_reaction("✅")
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
@commands.has_permissions(administrator=True)
async def censor(ctx):
    await ctx.message.add_reaction("✅")
    Server = str(ctx.guild.id)
    all_data.child('censor').update({Server: True})
    await ctx.send('I am now censored for this server')


# ----------------------------------------------------
@bot.command(name='uncensor')
@commands.has_permissions(administrator=True)
async def uncensor(ctx):
    await ctx.message.add_reaction("✅")
    Server = str(ctx.guild.id)
    all_data.child('censor').update({Server: False})
    await ctx.send('I am now uncensored for this server')


# ----------------------------------------------------

@bot.command(name='allroast')
async def allroast(ctx):
    await ctx.message.add_reaction("✅")
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
    await ctx.message.add_reaction("✅")
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
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(TOKEN)