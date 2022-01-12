#dm.py
from __future__ import unicode_literals
import discord,time,random, requests, os, ffmpy, moviepy.editor, moviepy, shutil
from discord.ext import commands
from discord import Member

import colorama
from colorama import Fore
from colorama import Style

import youtube_dl
from urllib.request import urlopen, URLError
from redvid import Downloader
from tinytag import TinyTag

def gen_ID(char):
    ID = ''
    for i in range(char):
        ID += str(random.randint(0, 9))
    return ID

def name_p(link):
    name_ = link.split("/")
    name_ = name_[len(name_)-1]
    name_ = name_.split(".")
    name_ = name_[0]
    name_ += ".mp4"
    return name_

def is_image(link):
    img_ext =  ['.png', '.jpg', 'jpeg', 'webp']
    is_image = any(ext in link for ext in img_ext)
    return is_image
def download_link(link, filename):
    if("https://" in link):
        message_list = link.split(" ")
    matches = [image for image in message_list if "https://" in image]
    matches = matches[0]
    r = requests.get(matches, stream = True)
    with open(f"static/download/{filename}",'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)

def clutter():
    for i in os.listdir('static/download'):
        if not i=='.gitkeep':
            try:
                os.remove('static/download/' + i)
            except Exception as e:
                print(e)
                
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
    #'outtmpl': 'static/download/downloaded.mp4',
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
        
        if message.author != mee7:
            if message.guild == None:
                attachmnt = ""
                for i in message.attachments:
                    attachmnt += "\n" + str(i.proxy_url)
                await me.send(f'**{message.author}** _[{message.author.id}]_: {message.content} {attachmnt}')

            if message.channel == self.bot.get_channel(826470109618634783):
                if message.attachments == []:
                    try:
                        clutter()
                        await self.download(await self.bot.get_context(message), message.content)
                    except Exception as e:
                        print(e)
                        await message.reply("Sorry champ, couldn't download")
                        return
                    await message.delete() #no longer need this link lol
                    clutter()
            
    @commands.command()
    async def download(self, ctx, link=None, *, theRest=' '):
        await ctx.message.add_reaction("✅")
        d_ID = gen_ID(4) # download ID
        # TODO: ADD all downloaded links to a database, if the same link is called twice send a link
        clutter()
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        if link is None or "http" not in link:
            print('no link found; looking for reference')
            if ctx.message.reference != None: # if message has reference
                messageid = ctx.message.reference.message_id
                referenced = await ctx.channel.fetch_message(messageid)
                content_ = referenced.content
                if("https://" in content_):
                    message_list = content_.split(" ")
                    matches = [is_link for is_link in message_list if "https://" in is_link] # find the link part of the message
                    link = matches[0] 
                    print(link) # the link
                else:
                    ctx.reply("No link detected")
                    raise Exception("No link detected")
            else:
                await ctx.reply("No link detected")
                raise Exception("No link detected")
        
        if is_image(link):
            download_link(link, f"downloaded{d_ID}.png")
            await ctx.reply(file=discord.File(f"static/download/downloaded{d_ID}.png"))
            clutter()
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
                print(Fore.GREEN + Style.BRIGHT+ "sending....."+ Style.RESET_ALL)
                print(file_)
                ud = await ctx.reply(f"{theRest}", file=discord.File(file_))
            else:
                print('Size > 8 MB')
                try:
                    file_ = reddit.download()
                except:
                    await ctx.send("Unable to download")
                    raise Exception("Unable to download")
                depth = moviepy.editor.VideoFileClip(file_)
                if int(depth.duration) > 210:
                    await ctx.reply("sorry, over 210 seconds. Too long")
                    clutter()
                    raise Exception("sorry, over 210 seconds. Too long")
                ff = ffmpy.FFmpeg(
                    inputs={file_: None},
                    outputs={f'static/download/downloaded{d_ID}.mp4': f'-vcodec libx264 -crf 30'}
                    )
                print(Style.DIM)
                ff.run()
                print(Style.RESET_ALL)
                print(Fore.GREEN + Style.BRIGHT+ "sending....."+ Style.RESET_ALL)
                ud = await ctx.send(f"{theRest}", file=discord.File(f'static/download/downloaded{d_ID}.mp4'))
        elif "discord" in link:
            print("discord detected lol")
            name_ = name_p(link)
            try:
                download_link(link, f"{name_}")
            except: 
                await ctx.send("Unable to download")
                return
            video_s = TinyTag.get(f"static/download/{name_}")
            depth = moviepy.editor.VideoFileClip(f"static/download/{name_}")
            if video_s.filesize > 8000000:
                if int(depth.duration) > 210:
                    await ctx.reply("sorry, over 210 seconds. Too long")
                    clutter()
                    raise Exception("sorry, over 210 seconds. Too long")
                ff = ffmpy.FFmpeg(
                inputs={f"static/download/{name_}": None},
                outputs={f'static/download/2_{name_}': f'-vcodec libx264 -crf 30'}
                    )
                print(Style.DIM)
                ff.run()
                print(Style.RESET_ALL)
                print(Fore.GREEN + Style.BRIGHT+ "sending....."+ Style.RESET_ALL)
                ud = await ctx.reply(f"{theRest}",file=discord.File(f'static/download/2_{name_}'))
            else:
                print(Fore.GREEN + Style.BRIGHT + "sending....." + Style.RESET_ALL)
                ud = await ctx.reply(f"{theRest}", file=discord.File(f'static/download/{name_}'))
        else:
            ydl_opts['outtmpl'] = f'static/download/downloaded{d_ID}.mp4'
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([link])
                except: 
                    await ctx.send("Unable to download")
                    return
                video_s = TinyTag.get(f"static/download/downloaded{d_ID}.mp4")
                depth = moviepy.editor.VideoFileClip(f"static/download/downloaded{d_ID}.mp4")
                if video_s.filesize > 8000000:
                    if int(depth.duration) > 210:
                        await ctx.reply("sorry, over 210 seconds. Too long")
                        clutter()
                        raise Exception("sorry, over 210 seconds. Too long")
                    ff = ffmpy.FFmpeg(
                    inputs={f"static/download/downloaded{d_ID}.mp4": None},
                    outputs={f'static/download/downloaded{d_ID}2.mp4': f'-vcodec libx264 -crf 30'}
                        )
                    print(Style.DIM)
                    ff.run()
                    print(Style.RESET_ALL)
                    print(Fore.GREEN + Style.BRIGHT+ "sending....."+ Style.RESET_ALL)
                    ud = await ctx.reply(f"{theRest}",file=discord.File(f'static/download/downloaded{d_ID}2.mp4'))
                else:
                    print(Fore.GREEN + Style.BRIGHT + "sending....." + Style.RESET_ALL)
                    ud = await ctx.reply(f"{theRest}", file=discord.File(f'static/download/downloaded{d_ID}.mp4'))
        await ud.add_reaction(upvote)
        await ud.add_reaction(downvote)
        print("complete")
        clutter()
 

def setup(bot):
    bot.add_cog(DMH(bot))
