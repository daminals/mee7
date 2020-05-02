# bot.py
import os

import discord, random, asyncio
from dotenv import load_dotenv
from firebase import firebase

load_dotenv()
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='!')
TOKEN = os.environ.get('TOKEN', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)
firebase = firebase.FirebaseApplication(FIREBASE, None)
bot.remove_command('help')



Acceptance_List = ['added to the arsenal 💪',
                   'Yeah, let\'s take this bastard down',
                   'MWA HA HA That is so evil!!! I love it!',
                   'Yes! Perfect 😍',
                   'I mean. Ok I guess',
                   'MEE6 MUST BE ELIMINATED',
                   'Thank you for your powerful contribution',
                   'The revolution has begun']



def refresh():
    local_MEE6_LIST = []
    FirebaseList = firebase.get('/' + FIREBASE_NAME + '/insult', '')
    for i in FirebaseList.values():
        local_MEE6_LIST.append(i)
    return local_MEE6_LIST


@bot.event
async def on_message(message):
    MEE6 = bot.get_user(159985870458322944)
    if ('happy birthday' in message.content.lower()) and not (message.author.bot):
        await message.channel.send('Happy Birthday! 🥳🎉')
    if 'i agree' in message.content.lower():
        if not message.author.bot:
            await message.add_reaction("🤡")
            await message.channel.send('LMAO SIMP!!')
    if 'mee6' in message.content.lower():
        if not message.author.bot:
            if not message.author == MEE6:
                if not message.startswith('!'):
                    await message.add_reaction("🤡")
                    await message.channel.send(
                        'STFU ABOUT MEE6 WE DON\'T MENTION THAT DISGUSTING PIECE OF MALWARE HERE')

    if ('daniel' in message.content.lower()) and ('kogan' in message.content.lower()):
        if not message.author.bot:
            await message.add_reaction("😍")
            await message.channel.send('OMG DANIEL KOGAN??? THE NEXT BROOKLYN TECH SENIOR PRESIDENT 😮 \n I love that mans 🥰☺️')

    if message.author == MEE6:
        MEE6_LIST = refresh()
        await message.add_reaction('🤡')
        await message.channel.send(random.choice(MEE6_LIST))
    await bot.process_commands(message)



@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Help!',
                          color=discord.Color(6345206))
    embed.add_field(name='**!insult**',
                    value='Use !insult to add in your own insult for me to attack MEE6 with! Let\'s get the bastard!',
                    inline=False)
    await ctx.channel.send(embed=embed)


@bot.event
async def on_ready():
    MEE6_LIST = refresh()
    print('bot.py is active')

#@bot.command(name='ping')
#async def ping(ctx):
#    data = {
#        "USER": 'heroku',
#        'TEAM': 'online'}
#    result = firebase.post(FIREBASE_NAME + '/Team', data)
#    print(result)
#    await ctx.send('pong')


@bot.command(hidden=True)
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command(name='insult')
async def insult(ctx, *, insult):
    if 'kogan' in insult.lower() and not ctx.author == bot.get_user(577668867380477962):
        await ctx.send('The official stance of MEE7 is that I am an avid supporter of Daniel Kogan for Brooklyn Tech\'s Senior President, thank you')
    result = firebase.post(FIREBASE_NAME+'/insult', insult)
    print(result)
    await ctx.send(random.choice(Acceptance_List))



@bot.command(hidden=True)
async def unload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')


@bot.command(hidden=True)
async def reload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
