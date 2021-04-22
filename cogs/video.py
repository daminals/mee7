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


def add_topv(vid, caption, Fw, h):
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

def deepfryv(vid, repeat):
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
                            
        
        
def setup(bot):
    bot.add_cog(Video(bot))
