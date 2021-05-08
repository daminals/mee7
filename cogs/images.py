#images.py
import discord,time,random,sys,os, os,ffmpy,moviepy.editor, requests,shutil
from discord.ext import commands
from discord import Member
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from random import randint, random, uniform

import colorama, moviepy
from colorama import Fore
from colorama import Style

sys.path.append(os.path.abspath('../'))
from bot import firebase, FIREBASE_NAME
# TODO: Stitch two images together
# TODO: speed up a video

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

def download_link(referenced, filename):
    if("https://" in referenced.content):
        message_list = referenced.content.split(" ")
    matches = [image for image in message_list if "https://" in image]
    matches = matches[0]
    r = requests.get(matches, stream = True)
    with open(f"static/created/{filename}",'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)

def is_image(referenced):
    img_ext =  ['.png', '.jpg', 'jpeg', 'webp']
    try: 
        is_image = get_attach(referenced).filename[-4:] in img_ext
    except:
        is_image = any(ext in referenced.content for ext in img_ext)
    return is_image

def is_video(referenced):
    vid_ext =  ['.mp4', '.mov', '.gif']
    try: 
        is_vid = get_attach(referenced).filename[-4:] in vid_ext
    except:
        is_vid = any(ext in referenced.content for ext in vid_ext)
    return is_vid

def converting_ffmpy(inputV, outputV):
    ff = ffmpy.FFmpeg(
    inputs={inputV: None},
    outputs={outputV: f'-vcodec libx264 -crf 30'}
        )
    print(Style.DIM)
    ff.run()
    print(Style.RESET_ALL)

def fast_forward(inputV, outputV, speed):
    newSpeed = round(1/speed, 2)
    ff = ffmpy.FFmpeg(
    inputs={inputV: None},
    outputs={outputV: f'-filter:a atempo={speed} -filter:v "setpts={newSpeed}*PTS" -vcodec libx264 -crf 30'}
        )
    print(Style.DIM)
    ff.run()
    print(Style.RESET_ALL)

async def check_refs_(ref, filename):
    print("Checking References")
    if ref.reference is not None: 
        #print("running 2")
        messageid = ref.reference.message_id
        referenced = await ref.channel.fetch_message(messageid)
        #print("running 3")
        await downloadM_(referenced, f"{filename}")
    else:
        #print("running 2")
        await downloadM_(ref, f"{filename}")

async def imgVidRefs(message):
    if message.reference != None: 
        messageid = message.reference.message_id
        referenced = await message.channel.fetch_message(messageid)
        return referenced
    else:
        if get_attach(message) != 0:
            referenced = message
            return referenced
        else:
            await message.reply("Sorry! No reference!")
            raise Exception("No references detected")


async def video_crefs(ref,filename,duration=210):
    await check_refs_(ref,filename)
    checkLength(filename, duration)
        
def checkLength(filename, duration=210):
    MovieClip = moviepy.editor.VideoFileClip(f"static/created/{filename}")
    if int(MovieClip.duration) > duration:
        raise Exception(f"Video over {duration} seconds")  
    return MovieClip

    
async def upvDownv(bot, ud, message):
    downvote = bot.get_emoji(776162465842200617)
    upvote = bot.get_emoji(776161705960931399)
    try:
        await ud.add_reaction(upvote)
        await ud.add_reaction(downvote)
    except Exception as e:
        print(exit)
        await message.reply("no")
    clutter()

    
# ------------------ IMAGE MANIPULATION -------------------

# TODO: VIRGIN VS CHAD MEME TEMPLATE 

def image_text(img, title_text, x, y, font_size,ext="png", color=(237, 230, 211), font='static/fonts/arial-black.ttf'):
    my_image = Image.open(f"static/{img}.{ext}")
    title_font = ImageFont.truetype(font, font_size) # can make further robust and change fonts if needed
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((x,y), title_text, color, font=title_font)
    my_image.save(f"static/created/{title_text}.{ext}")
    
def alwaysHasBeen(title_text):
    # TODO: make location and stuff based on size, as well as breaking up txt into lines
    image_text("ahb",title_text, 400,175,15,"png")

def mirror(user_disc):
    image_text("mirror", user_disc, 175,175,30,"jpg",(0,0,0))

# ---------------------------------------------------------------

def get_attach(message):
    return message.attachments[0]

def clutter():
    for i in os.listdir('static/created'):
        if not i=='.gitkeep':
            os.remove('static/created/' + i)

def add_top(img,caption):
    caption = caption.upper()
    print("loading image")
    current = Image.open(img)
    ch = current.height
    difference = current.height
    cw = current.width
    ch *= 1.2
    ch = int(ch)
    difference = ch - difference
    print(Fore.RED + Style.BRIGHT + "making new image 💄" + Style.RESET_ALL)
    top = Image.new('RGBA', (cw,ch), 'white')
    top.paste(current, (0,difference))
    
    print("captioning")
    font_size = int(cw*0.085)
    font = ImageFont.truetype('static/fonts/impact.ttf', font_size)
    image_editable = ImageDraw.Draw(top)
    w,h = image_editable.textsize(caption, font=font)
    
    temp = cw / w
    temp *= 0.85
    font_size *= temp
    font_size = int(font_size)
    font = ImageFont.truetype('static/fonts/impact.ttf', font_size)
    w,h = image_editable.textsize(caption, font=font)
    
    if h > difference:
        hedit = h
        ch -= difference
        hedit += int(difference * 0.25)
        ch += hedit
        top = Image.new('RGBA', (cw,ch), 'white')
        font = ImageFont.truetype('static/fonts/impact.ttf', font_size)
        w,h = image_editable.textsize(caption, font=font)
        image_editable = ImageDraw.Draw(top)
        top.paste(current, (0,hedit))
        difference = current.height
        difference = ch - difference
    
    image_editable.text(((cw - w)/2,(difference-h)/2), caption, (0,0,0), font=font)
    top.save(img, optimize=True)
    print("image created")

async def downloadM_(referenced, filename):
    try: 
        await get_attach(referenced).save(f"static/created/{filename}")
        print("attachment received")
    except:
        print(referenced.content)
        download_link(referenced, f"{filename}")
    print("Downloaded") 
    return f"static/created/{filename}"


# ------------------- DEEP FRY ------------------

def deepfryi(img):
    current = Image.open(img)
    current = current.filter(ImageFilter.UnsharpMask(radius=randint(5,20),percent=randint(105,550),threshold=randint(1,5)))
    layer = Image.new(current.mode, current.size, 'red') # "hue" selection is done by choosing a color...
    current = Image.blend(current, layer, 0.20)
    for i in range(2):
        current = current.filter(ImageFilter.UnsharpMask(radius=randint(5,25),percent=randint(105,550),threshold=randint(1,5)))
    current.save(img)

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.upvote = self.bot.get_emoji(776161705960931399)
        self.downvote = self.bot.get_emoji(776162465842200617)

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.MAGENTA + Style.BRIGHT  + 'images.py is active' + Style.RESET_ALL)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        
        # ----------- MIRROR MIRROR --------------------------
        
        if "mirror mirror on the wall whos the upvotedest of them all" in message.content.lower():
            basedCount = firebase.get('/' + FIREBASE_NAME + '/upvotecount/', '')
            basedest = 0
            basedestp = ""
            for based_users in basedCount.items():
                #await message.channel.send(based_users)
                user, count = based_users
                thePerson = self.bot.get_user(int(user))
                if thePerson in message.guild.members:
                    if count > basedest:
                        basedest = count
                        basedestp = thePerson
                        #await message.channel.send(f"{basedest}, {basedestp}")
            user = str(basedestp.name) + '#' + str(basedestp.discriminator)
            mirror(user)
            ud = await message.reply(file=discord.File(f"static/created/{user}.jpg"))
            await ud.add_reaction(upvote)
            await ud.add_reaction(downvote)
            return
                
        if "mirror mirror on the wall whos the basedest of them all" in message.content.lower():
            basedCount = firebase.get('/' + FIREBASE_NAME + '/basedcount/', '')
            basedest = 0
            basedestp = ""
            for based_users in basedCount.items():
                #await message.channel.send(based_users)
                user, count = based_users
                thePerson = self.bot.get_user(int(user))
                if thePerson in message.guild.members:
                    if count > basedest:
                        basedest = count
                        basedestp = thePerson
                        #await message.channel.send(f"{basedest}, {basedestp}")
            user = str(basedestp.name) + '#' + str(basedestp.discriminator)
            mirror(user)
            ud = await message.reply(file=discord.File(f"static/created/{user}.jpg"))
            await ud.add_reaction(upvote)
            await ud.add_reaction(downvote)
            return
    
        if "mirror mirror on the wall who" in message.content.lower():
            server = message.guild
            all_members = server.members
            member = random.choice(all_members)
            user = str(member.name) + '#' + str(member.discriminator)
            mirror(user)
            ud = await message.reply(file=discord.File(f"static/created/{user}.jpg"))
            await ud.add_reaction(upvote)
            await ud.add_reaction(downvote)
                
                
        # -----------------------------------------------------------------
        
        if message.reference != None: # if message has reference
                messageid = message.reference.message_id
                referenced = await message.channel.fetch_message(messageid)
                
                # --------------- ALWAYS HAS BEEN ---------------------------
                
                if "always has been" in message.content.lower():
                    content = referenced.content
                    alwaysHasBeen(content)
                    ud = await message.reply(file=discord.File(f"static/created/{content}.png"))
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)

        
    @commands.command()
    async def av(self,ctx, member: Member=None):
        if member == None:
            member = ctx.author
        await ctx.channel.send(member.avatar_url)
    
    @commands.command()
    async def deepfry(self, ctx, repeat=1): 
        try:
            repeat = int(repeat)
        except:
            await ctx.reply("Command paramaters used incorrectly.")
        referenced = await imgVidRefs(ctx.message)        
        print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
        print(Style.BRIGHT+f"Call me McDonalds cuz be be deep fryin this mf {repeat} times"+Style.RESET_ALL)
        # check -- is this an image? can I download it?
        if is_image(referenced):
            if repeat > 20: repeat = 20 # set 20 as the deepfry limit
            await downloadM_(referenced, f"deepfry.png")            
            for i in range(repeat):
                deepfryi(f"static/created/deepfry.png")
                print(Style.DIM+ f"deepfried it {i+1} times bestie" + Style.RESET_ALL)
            print(Fore.YELLOW + Style.BRIGHT + "sending image ⏳"+ Style.RESET_ALL)
            ud = await ctx.reply(file=discord.File(f"static/created/deepfry.png"))
            print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
        elif is_video(referenced):
            if repeat > 4: repeat = 4 # set 4 as the deepfry limit
            await downloadM_(referenced, f"deepfried0.mp4") # downloads video
            checkLength("deepfried0.mp4",60) # throws exception if video is too long
            for i in range(repeat):
                deepfryv(f"static/created/deepfried{i}.mp4", i)
                print(Style.DIM+ f"deepfried it {i+1} times bestie" + Style.RESET_ALL)
            print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
            ud = await ctx.reply(file=discord.File(f"static/created/deepfried{repeat}.mp4"))
            print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
        await upvDownv(self.bot,ud,ctx.message)

        
    @commands.command(aliases=["caption:"])
    async def caption(self, ctx, *, caption):        
        # if message has reference -- no reference no caption
        caption = caption.upper()
        referenced = await imgVidRefs(ctx.message)        
        print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "downloading attachment ⏳" + Style.RESET_ALL)
        
        # is this an image? can I download it?
        if is_image(referenced):
            await downloadM_(referenced, f"{caption[:2]}.png")
            # ok, caption this image lol
            add_top(f"static/created/{caption[:2]}.png",caption)
            print(Fore.YELLOW + Style.BRIGHT + "sending image ⏳"+ Style.RESET_ALL)
            ud = await ctx.reply(file=discord.File(f"static/created/{caption[:2]}.png"))
            print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
      
        # is this a video? can I download it?    
        elif is_video(referenced):
            await downloadM_(referenced, f"{caption[:2]}.mp4")
            captionClip = checkLength(f"{caption[:2]}.mp4",60) # throws exception if video is too long
            add_topv(f"static/created/{caption[:2]}.mp4",caption,captionClip.w,captionClip.h)
            print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
            ud = await ctx.reply(file=discord.File(f"static/created/captioned.mp4"))
            print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
        await upvDownv(self.bot, ud, ctx.message)

    @commands.command(name="convert")
    async def convert(self, ctx, *, link=None):
        clutter()
        # logging
        print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "downloading attachment ⏳" + Style.RESET_ALL)
        # download
        await video_crefs(ctx.message, f"convert.mp4")
        converting_ffmpy("static/created/convert.mp4", "static/created/converted.mp4")
        # send vid
        print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
        ud = await ctx.reply(file=discord.File(f"static/created/converted.mp4"))
        print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
        await upvDownv(self.bot, ud, ctx.message)

    @commands.command(name="speed")
    async def speed(self,ctx, spd, link=None):
        spd = float(spd)
        clutter()
        # logging
        print(Fore.RED + Style.BRIGHT+"\n---------------\n"+Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "downloading attachment ⏳" + Style.RESET_ALL)
        # download
        try:
            await video_crefs(ctx.message, "spd.mp4")
        except Exception as e:
            print(e)
            await ctx.reply("sorry bestie, but that video is over 210 seconds. I won't do it")
            return
        fast_forward("static/created/spd.mp4","static/created/newSpeed.mp4",spd)
        print(Fore.YELLOW + Style.BRIGHT + "sending video ⏳"+ Style.RESET_ALL)
        ud = await ctx.reply(file=discord.File(f"static/created/newSpeed.mp4"))
        print(Fore.GREEN + Style.BRIGHT + "complete ✔︎ " + Style.RESET_ALL)
        await upvDownv(self.bot,ud,ctx.message)
        
    @commands.command(name="layered")
    async def layered(self,ctx, commands, link=None):
        pass
        
        
def setup(bot):
    bot.add_cog(Images(bot))
