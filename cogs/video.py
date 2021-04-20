#video.py
import discord,time,random,sys,os,ffmpy
from discord.ext import commands
from discord import Member
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from random import randint, random, uniform
from shutil import copyfile, rmtree

import colorama
from colorama import Fore
from colorama import Style

sys.path.append(os.path.abspath('../'))
from bot import firebase, FIREBASE_NAME

def get_attach(message):
    return message.attachments[0]

def deepfry(vid, repeat):
    ff = ffmpy.FFmpeg(
     inputs={vid: None},
     outputs={f'static/created/deepfried{repeat+1}.mp4': f'{create_filter_args()} {create_audio_args(repeat)}-vcodec libx264 -crf 45'}
    )
    ff.run()

def create_audio_args(repeat):
    if repeat >= 1:
        return ""
    else:
        return '-af ' + 'bass=g=18,treble=g=2,volume=10dB,' + 'acompressor=threshold=0.02:makeup=15,acontrast=79 '

def create_filter_args():
    """
    Create randomized "deep fried" visual filters
    returns command line args for ffmpeg's filter flag -vf
    """
    saturation = uniform(2, 3)
    contrast = uniform(.5, 2)
    noise = uniform(30, 60)
    gamma_r = uniform(1, 3)
    gamma_g = uniform(1, 3)
    gamma_b = uniform(1, 3)

    eq_str = 'eq=saturation={}:contrast={}'.format(saturation, contrast)
    eq_str += ':gamma_r={}:gamma_g={}:gamma_b={}'.format(gamma_r, gamma_g, gamma_b)
    noise_str = 'noise=alls={}:allf=t'.format(noise)
    sharpness_str = 'unsharp=5:5:1.25:5:5:1'

    return '-vf ' + eq_str + ',' + noise_str + ',' + sharpness_str


class Video(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + Style.BRIGHT  + 'video.py is active' + Style.RESET_ALL)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)

        # -----------------------------------------------------------------
        
        if message.reference != None: # if message has reference
                messageid = message.reference.message_id
                referenced = await message.channel.fetch_message(messageid)
            
                    
                # ------------------ ADD HEADER ------------------------------
                """
                if "caption:" in message.content.lower():
                    print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
                    caption = message.content[9:].upper()
                    print(caption)
                    #await message.channel.send(caption)
                    print(Fore.YELLOW + Style.BRIGHT + "downloading attachment ⏳" + Style.RESET_ALL)
                    await get_attach(referenced).save(f"static/created/{caption[:2]}.png")
                    add_top(f"static/created/{caption[:2]}.png",caption)
                    print(Fore.YELLOW + Style.BRIGHT + "sending image ⏳"+ Style.RESET_ALL)
                    ud = await message.reply(file=discord.File(f"static/created/{caption[:2]}.png"))
                    print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)
                """
                # ------------------ DEEP FRYER ------------------------------

                if "deepfry" in message.content.lower():
                    print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
                    repeat = 1
                    if message.content[7:]:
                        repeat = int(message.content[8:])
                        if repeat > 4: repeat = 4
                    print(Style.BRIGHT+f"Call me McDonalds cuz be be deep fryin this mf {repeat} times"+Style.RESET_ALL)
                    if get_attach(referenced).filename[-4:] in ['.mov', '.mp4']:
                        await get_attach(referenced).save(f"static/created/deepfried0.mp4")
                    else:
                        print("not a video")
                        print(get_attach(referenced).filename[-4:])
                        return
                    for i in range(repeat):
                        deepfry(f"static/created/deepfried{i}.mp4", i)
                        print(Style.DIM+ f"deepfried it {i+1} times bestie" + Style.RESET_ALL)
                    print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
                    ud = await message.reply(file=discord.File(f"static/created/deepfried{repeat}.mp4"))
                    try:
                        for i in range(repeat+1):
                            os.remove(f'static/created/deepfried{i}.mp4')
                        os.remove('static/created/deepfry.png')
                    except:
                        print(Fore.RED + "could not remove videos" + Style.RESET_ALL)
                    print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)
                            
                
        
        
            
        
        
        
def setup(bot):
    bot.add_cog(Video(bot))
