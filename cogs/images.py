#exec.py
import discord,time,random
from discord.ext import commands
from discord import Member
from PIL import Image, ImageFilter, ImageFont, ImageDraw

def image_text(img, title_text, x, y, font_size,ext="png", color=(237, 230, 211)):
    my_image = Image.open(f"static/{img}.{ext}")
    title_font = ImageFont.truetype('static/fonts/arial-black.ttf', font_size) # can make further robust and change fonts if needed
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((x,y), title_text, color, font=title_font)
    my_image.save(f"static/{title_text}.{ext}")
    
def alwaysHasBeen(title_text):
    # TODO: make location and stuff based on size, as well as breaking up txt into lines
    image_text("ahb",title_text, 400,175,15,"png")

def mirror(user_disc):
    # TODO: whenever someone says mirror mirror on the wall whos the {} of them all, return a random user on a mirror pic
    image_text("mirror", user_disc, 175,175,30,"jpg",(0,0,0))

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
        
        
        if "mirror mirror on the wall who" in message.content:
            server = message.guild
            all_members = server.members
            member = random.choice(all_members)
            user = str(member.name) + '#' + str(member.discriminator)
            mirror(user)
            ud = await message.reply(file=discord.File(f"static/{user}.jpg"))
            await ud.add_reaction(upvote)
            await ud.add_reaction(downvote)
        
        if message.reference != None: # if message has reference
                messageid = message.reference.message_id
                referenced = await message.channel.fetch_message(messageid)
                if "always has been" in message.content.lower():
                    content = referenced.content
                    alwaysHasBeen(content)
                    ud = await message.reply(file=discord.File(f"static/{content}.png"))
                    await ud.add_reaction(upvote)
                    await ud.add_reaction(downvote)
                    
            
        
    
        
        
        
def setup(bot):
    bot.add_cog(Images(bot))
