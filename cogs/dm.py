#exec.py
from __future__ import unicode_literals
import discord,time,random, requests, os, ffmpy, moviepy.editor, moviepy
from discord.ext import commands
from discord import Member

import colorama
from colorama import Fore
from colorama import Style

import youtube_dl
from urllib.request import urlopen, URLError
from redvid import Downloader
from tinytag import TinyTag


def clutter():
    for i in os.listdir('static/download'):
        if not i=='.gitkeep':
            os.remove('static/download/' + i)
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'mp4',
    'outtmpl': 'static/download/downloaded.mp4',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


class DMH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + Style.BRIGHT +'dm.py is active' + Style.RESET_ALL)

    @commands.Cog.listener()
    async def on_message(self, message):
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        MEE6 = self.bot.get_user(159985870458322944)
        me = self.bot.get_user(577668867380477962)
        mee7 = self.bot.get_user(706194661366300753)
        channel_ = self.bot.get_channel(825724511831457813)
        
        if message.guild == None and message.author != mee7:
            attachmnt = ""
            for i in message.attachments:
                attachmnt += "\n" + str(i.proxy_url)
            await me.send(f'**{message.author}** _[{message.author.id}]_: {message.content} {attachmnt}')
            
            if "reddit" in message.content and message.author == me:  
                reddit = Downloader(max_q=True)
                reddit.path = 'static/download'
                reddit.url = message.content
                reddit.check()
                if reddit.size <= 8 * (1 << 20):
                    file_ = reddit.download()
                    await channel_.send(file=discord.File(file_))
                else:
                    print('Size > 8 MB')
                    file_ = reddit.download()
                    depth = moviepy.editor.VideoFileClip(file_)
                    if int(depth.duration) > 210:
                        await message.reply("sorry, over 210 seconds. Too long")
                        clutter()
                        return
                    ff = ffmpy.FFmpeg(
                        inputs={file_: None},
                        outputs={f'static/download/downloaded.mp4': f'-vcodec libx264 -crf 30'}
                        )
                    ff.run()
                    await channel_.send(file=discord.File('static/download/downloaded.mp4'))
                clutter()

    @commands.command()
    async def download(self, ctx, link=None):
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        if link is None:
            if ctx.reference != None: # if message has reference
                messageid = ctx.reference.message_id
                referenced = await ctx.channel.fetch_message(messageid)
                link = referenced.content
            else:
                await ctx.reply("No link detected")
                return
        print("\nrunning....")
        if "reddit" in link:  
            print("reddit detected....")
            reddit = Downloader(max_q=True)
            reddit.path = 'static/download'
            reddit.url = link
            reddit.check()
            if reddit.size <= 8 * (1 << 20):
                file_ = reddit.download()
                ud = await ctx.reply(file=discord.File(file_))
            else:
                print('Size > 8 MB')
                file_ = reddit.download()
                depth = moviepy.editor.VideoFileClip(file_)
                if int(depth.duration) > 210:
                    await ctx.reply("sorry, over 210 seconds. Too long")
                    clutter()
                    return
                ff = ffmpy.FFmpeg(
                    inputs={file_: None},
                    outputs={f'static/download/downloaded.mp4': f'-vcodec libx264 -crf 30'}
                    )
                ff.run()
                print("sending.....")
                ud = await ctx.send(file=discord.File('static/download/downloaded.mp4'))
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
                video_s = TinyTag.get("static/download/downloaded.mp4")
                depth = moviepy.editor.VideoFileClip("static/download/downloaded.mp4")
                if video_s.filesize > 8000000:
                    if int(depth.duration) > 210:
                        await ctx.reply("sorry, over 210 seconds. Too long")
                        clutter()
                        return
                    ff = ffmpy.FFmpeg(
                    inputs={"static/download/downloaded.mp4": None},
                    outputs={f'static/download/downloaded2.mp4': f'-vcodec libx264 -crf 30'}
                        )
                    ff.run()
                    print("sending.....")
                    ud = await ctx.reply(file=discord.File('static/download/downloaded2.mp4'))
                else:
                    print("sending.....")
                    ud = await ctx.reply(file=discord.File('static/download/downloaded.mp4'))
        await ud.add_reaction(upvote)
        await ud.add_reaction(downvote)
        clutter()


def setup(bot):
    bot.add_cog(DMH(bot))
