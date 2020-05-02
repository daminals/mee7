# bot.py
import os

import discord, random, asyncio
from dotenv import load_dotenv
from discord import Member
from itertools import cycle

load_dotenv()
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='!', description='Aejay\'s Birthday!!')
TOKEN = os.environ.get('TOKEN', 3)


@bot.event
async def on_ready():
    party = bot.get_emoji(698725283649290310)
    bot_channel = bot.get_channel(689168363083268249)
    user = bot.get_user(340996105460514816)
    # 340996105460514816 - Aejay
    # 577668867380477962 - me
    background_task.start(user, bot_channel)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Aejay... Constantly", emoji=party))
    print('bot.py is active')


global_speed = 60*15


@bot.event
async def on_message(message):
    if message.channel == bot.get_channel(689168363083268249):
        emoji = '🥳'
        emoji2 = '🎉'
        await message.add_reaction(emoji)
        await message.add_reaction(emoji2)
    else:
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


@bot.command(name='speed')
async def speed(ctx, speed):
    await bot.wait_until_ready()
    await ctx.channel.send('lmfao i have no clue why im bbroken teehee')
    if ctx.message.author == bot.get_user(340996105460514816):
        await ctx.channel.send(f'{bot.get_user(340996105460514816)} cannot use this command')
        return
    global global_speed
    global_speed = speed
    await ctx.send(f'speed updated to {speed}')


@tasks.loop(seconds=global_speed)
async def background_task(user, bot_channel):
    await bot.wait_until_ready()
    await bot_channel.send(f'Happy Birthday {user.mention}! 🥳🎉')
    print('happy brithday')


@bot.command(name='tracking')
async def tracking(ctx):
    embed = discord.Embed(title='Tracking:', description=f'{global_speed}')
    await ctx.channel.send(embed=embed)


@bot.command(hidden=True)
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


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
