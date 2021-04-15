#exec.py
import discord,time,random
from discord.ext import commands
from discord import Member
from PIL import Image, ImageFilter, ImageFont, ImageDraw

def image_text(img, title_text, x, y, font_size):
    my_image = Image.open(f"images/{img}.png")
    title_font = ImageFont.truetype('fonts/arial-black.ttf', font_size) # can make further robust and change fonts if needed
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((x,y), title_text, (237, 230, 211), font=title_font)
    my_image.save(f"images/{title_text}.png")
    
def alwaysHasBeen(title_text):
    # TODO: make location and stuff based on size, as well as breaking up txt into lines
    image_text("ahb",title_text, 400,175,15)



class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('images.py is active')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.reference != None: # if message has reference
                messageid = message.reference.message_id
                referenced = await message.channel.fetch_message(messageid)
                if "always has been" in message.content.lower():
                    content = referenced.content
                    alwaysHasBeen(content)
                    await message.reply(file=discord.File(f"images/{content}.png"))
                    
            
        
    
        
        
        
def setup(bot):
    bot.add_cog(Images(bot))
