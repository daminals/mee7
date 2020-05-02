# bot.py
import os

import discord, random, asyncio
from dotenv import load_dotenv
from discord import Member
from itertools import cycle
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


@bot.event
async def on_message(message):
        if random.randint(0, 100) > 99:
            emoji = '🥳'
            emoji2 = '🎉'
            await message.add_reaction(emoji)
            await message.add_reaction(emoji2)
        if ('happy birthday' in message.content.lower()) and not(message.author.bot):
            await message.channel.send('Happy Birthday! 🥳🎉')
        if random.randint(0, 100) > 99:
            await message.channel.send('Happy Birthday! 🥳🎉')
        if 'i agree' in message.content.lower():
            if not message.author.bot:
                await message.add_reaction("🤡")
                await message.channel.send('LMAO SIMP!!')
        if message.author == MEE6:
            await message.channel.send()

@bot.command(hidden=True)
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command(name='insult')
async def insult(ctx, *, insult):
    result = firebase.post(FIREBASE_NAME+'/insult', insult)
    print(result)


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
