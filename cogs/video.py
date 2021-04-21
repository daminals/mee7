#video.py
import discord,time,random,sys,os,ffmpy,moviepy.editor, requests, shutil
from discord.ext import commands
from discord import Member
from random import randint, random, uniform
from PIL import ImageFont

import colorama
from colorama import Fore
from colorama import Style

sys.path.append(os.path.abspath('../'))
from bot import firebase, FIREBASE_NAME

def clutter():
    for i in os.listdir('static/created'):
        if not i=='.gitkeep':
            os.remove('static/created/' + i)


def add_top(vid, caption, Fw, h):
    newH = h * 1.35
    placementH = h*0.35
    font_size = int(h * 0.1)
    caption = fit_text(caption, Fw, font_size)
    
    ff = ffmpy.FFmpeg(
     inputs={vid: None},
     outputs={f'static/created/captioned.mp4': f'-vf "pad=iw:{newH}:iw/2:{placementH}:color=white",drawtext="fontfile=static/fonts/impact.ttf":text="{caption}":fontcolor=black:fontsize={font_size}:x=(w-tw)/2:y=({placementH}-th)/2:fix_bounds=true:line_spacing=3 -vcodec libx264 -codec:a copy -crf 35'}
    )
    ff.run()

def fit_text(string: str, frame_width, font_size):
    split_line = [x.strip() for x in string.split()]
    translation_font = ImageFont.truetype("static/fonts/impact.ttf", size=font_size, encoding="unic")
    lines = ""
    w = 0
    line_num = 0
    line = ""
    for word in split_line:
        # Make a test
        w, _ = translation_font.getsize(" ".join([line, word]))
        # If it exceeds the frame width, add a new line
        if w > (frame_width - (2 * 4)):  # Leave 6px margin on each side
            lines += line.strip() + "\n"
            line = ""

        line += word + " "

    lines += line.strip()  # Append leftover words
    return lines


def get_attach(message):
    return message.attachments[0]

def deepfry(vid, repeat):
    ff = ffmpy.FFmpeg(
     inputs={vid: None},
     outputs={f'static/created/deepfried{repeat+1}.mp4': f'{create_filter_args()} {create_audio_args(repeat)}-vcodec libx264 -crf 45'}
    )
    ff.run()

def create_audio_args(repeat):
    return '-af ' + 'bass=g=18,treble=g=2,volume=10dB,' + 'acompressor=threshold=0.02:makeup=5,acontrast=45 '

def create_filter_args():
    """
    Create randomized "deep fried" visual filters
    returns command line args for ffmpeg's filter flag -vf
    """
    saturation = uniform(2, 5)
    contrast = uniform(1, 8)
    noise = uniform(5, 20)
    gamma_r = uniform(2, 3)
    gamma_g = uniform(1, 2)
    gamma_b = uniform(1, 1.5)

    eq_str = 'eq=saturation={}:contrast={}'.format(saturation, contrast)
    eq_str += ':gamma_r={}:gamma_g={}:gamma_b={}'.format(gamma_r, gamma_g, gamma_b)
    noise_str = 'noise=alls={}:allf=t'.format(noise)
    sharpness_str = 'unsharp=3:3:1.3:3:3:1.5'

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
                
                if "caption:" in message.content.lower():
                    print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
                    clutter()
                    caption = message.content[9:].upper()
                    print(caption)
                    #await message.channel.send(caption)
                    print(Fore.YELLOW + Style.BRIGHT + "downloading attachment ⏳" + Style.RESET_ALL)
                    try:
                        if get_attach(referenced).filename[-4:] in ['.mov', '.mp4','.gif']:
                            await get_attach(referenced).save(f"static/created/{caption[:2]}.mp4")
                        else:
                            print("not a video")
                            print(get_attach(referenced).filename[-4:])
                            return
                    except:
                        print(referenced.content)
                        if("https://" in referenced.content):
                            message_list = referenced.content.split(" ")
                            matches = [image for image in message_list if "https://" in image]
                            matches = matches[0]
                            r = requests.get(matches, stream = True)
                            with open(f"static/created/{caption[:2]}.mp4",'wb') as out_file:
                                for chunk in r.iter_content(chunk_size = 1024*1024): 
                                    if chunk: 
                                        out_file.write(chunk) 
                    
                    captionClip = moviepy.editor.VideoFileClip(f"static/created/{caption[:2]}.mp4")
                    if int(captionClip.duration) > 60:
                        await message.reply("sorry bestie, but that video is over a minute. I won't do it")
                        return     
                    add_top(f"static/created/{caption[:2]}.mp4",caption,captionClip.w,captionClip.h)
                    print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
                    ud = await message.reply(file=discord.File(f"static/created/captioned.mp4"))
                    print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)
                    clutter()
                    
                # ------------------ DEEP FRYER ------------------------------

                if "deepfry" in message.content.lower():
                    clutter()
                    print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
                    repeat = 1
                    if message.content[7:]:
                        try:
                            repeat = int(message.content[8:])
                            if repeat > 4: repeat = 4
                        except:
                            print("repeat failed. only once lol")
                    print(Style.BRIGHT+f"Call me McDonalds cuz be be deep fryin this mf {repeat} times"+Style.RESET_ALL)
                    try:
                        if get_attach(referenced).filename[-4:] in ['.mov', '.mp4','.gif']:
                            await get_attach(referenced).save(f"static/created/deepfried0.mp4")
                        else:
                            print("not a video")
                            print(get_attach(referenced).filename[-4:])
                            return
                    except:
                        print(referenced.content)
                        if("https://" in referenced.content):
                            message_list = referenced.content.split(" ")
                            matches = [image for image in message_list if "https://" in image]
                            matches = matches[0]
                            r = requests.get(matches, stream = True)
                            with open("static/created/deepfried0.mp4",'wb') as out_file:
                                for chunk in r.iter_content(chunk_size = 1024*1024): 
                                    if chunk: 
                                        out_file.write(chunk) 
                    
                    deep = moviepy.editor.VideoFileClip("static/created/deepfried0.mp4")
                    if int(deep.duration) > 60:
                        await message.reply("sorry bestie, but that video is over a minute. I won't do it")
                        return     
                    for i in range(repeat):
                        deepfry(f"static/created/deepfried{i}.mp4", i)
                        print(Style.DIM+ f"deepfried it {i+1} times bestie" + Style.RESET_ALL)
                    print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
                    ud = await message.reply(file=discord.File(f"static/created/deepfried{repeat}.mp4"))
                    try:
                        clutter()
                    except:
                        print(Fore.RED + "could not remove videos" + Style.RESET_ALL)
                    print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)
                            
                
        
        
            
        
        
        
def setup(bot):
    bot.add_cog(Video(bot))
