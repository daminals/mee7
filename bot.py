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

MEE6 = bot.get_user(159985870458322944)
firebase = firebase.FirebaseApplication(FIREBASE, None)



ListOfMEE6insults = []



@bot.event
async def on_ready():
    print('bot.py is active')



@bot.command(name='ping')
async def ping(ctx):
    data = {
        "USER": 'heroku',
        'TEAM': 'online'}
    result = firebase.post(FIREBASE_NAME + '/Team', data)
    print(result)
    await ctx.send('pong')


@bot.command(hidden=True)
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command(name='insult')
async def insult(ctx, *, insult):
    result = firebase.post(FIREBASE_NAME+'/insult', insult)
    print(result)
    bruh = firebase.get('/' + FIREBASE_NAME + '/insult', '')
    print(bruh)
    await ctx.send('bruh')



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
