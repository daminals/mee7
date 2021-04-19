#exec.py
import discord,time,random,sys,os
from discord.ext import commands
from discord import Member
from PIL import Image, ImageFilter, ImageFont, ImageDraw

sys.path.append(os.path.abspath('../'))
from bot import firebase, FIREBASE_NAME


# ------------------ IMAGE MANIPULATION -------------------

# TODO: VIRGIN VS CHAD MEME TEMPLATE 

def image_text(img, title_text, x, y, font_size,ext="png", color=(237, 230, 211)):
    my_image = Image.open(f"static/{img}.{ext}")
    title_font = ImageFont.truetype('static/fonts/arial-black.ttf', font_size) # can make further robust and change fonts if needed
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

def add_top(img):
    current = Image.open(img)
    ch = current.height
    cw = current.width
    ch += 40
    top = Image.new('RGBA', (ch,cw), 'white')
    top.save(img)




class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('images.py is active')
        
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
                    
                # ------------------ ADD HEADER ------------------------------
                
                if "caption:" in message.content.lower():
                    caption = message.content[9:].upper()
                    #await message.channel.send(caption)
                    await get_attach(referenced).save(f"static/saved/{caption[:5]}.png")
                    add_top(f"static/saved/{caption[:5]}.png")
                    await message.reply(file=discord.File(f"static/saved/{caption[:5]}.png"))
                    pass
                    
            
        
    
        
        
        
def setup(bot):
    bot.add_cog(Images(bot))
