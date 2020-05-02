# bot.py
import os

import discord, random, asyncio
from dotenv import load_dotenv
from firebase import firebase

load_dotenv()
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='!', description='Aejay\'s Birthday!!')
TOKEN = os.environ.get('TOKEN', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)
firebase = firebase.FirebaseApplication(FIREBASE, None)
bot.remove_command('help')



Acceptance_List = ['added to the arsenal 💪',
                   'Yeah let\'s take this bastard down',
                   'MWA HA HA That is so evil!!! I love it!',
                   'Yes! Perfect 😍',
                   'I mean. Ok I guess',
                   'MEE6 MUST BE ELIMINATED']

MEE6_LIST = []


@bot.command(name='refresh', hidden=True)
async def refresh(ctx):
    MEE6_LIST = []
    FirebaseList = firebase.get('/' + FIREBASE_NAME + '/insult', '')
    for i in FirebaseList.values():
        MEE6_LIST.append(i)


@bot.event
async def on_message(message):
    MEE6 = bot.get_user(159985870458322944)
    if ('happy birthday' in message.content.lower()) and not (message.author.bot):
        await message.channel.send('Happy Birthday! 🥳🎉')
    if 'i agree' in message.content.lower():
        if not message.author.bot:
            await message.add_reaction("🤡")
            await message.channel.send('LMAO SIMP!!')
    if message.author == MEE6:
        await refresh()
        await message.add_reaction('🤡')
        await message.channel.send(random.choice(MEE6_LIST))
    print(message.author)
    print(MEE6)
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await refresh()
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


bot.run(TOKEN)
