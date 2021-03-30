# fun.py
import discord, random, asyncio
from discord.ext import commands

emojis = ["😎", "😍", "😂", "🥶", "😱", "😳", "🤢", "🥱", "🤐", "🤯", "🤠", "💀", "🤏", "👀", "🌵", "⚡️", "💦", "🎉",
          "🥳", "😈", "🤡", "✅", "❌", "🤔", "🙄", "🥺", "🤧", "🆗", "💰", "🥰", "😜", "💪", "🤙", "👑", "✈️", "🇺🇸",
          "⛓", "🔪","😕","👺","🐸","💅","🤦‍♀️","💆‍♀️","🧏‍♀️","💁‍♀️","🤒","🤮","🤥","🤤","😬","😰","🤭","🤫","😓","🥺"]

# testing file lol
class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('fun.py is active')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if 'ugh fine' in message.content.lower():
            await message.reply('https://tenor.com/view/poggers-pogchamp-pog-meme-animation-gif-19294003')
            await message.add_reaction("🥺")
            await message.add_reaction("👉")
            await message.add_reaction("👈")
            return
        if 'ur mom' in message.content.lower():
            await message.reply('https://tenor.com/view/urmom-your-mom-baldi-defaultdance-gif-19665250')
            await message.add_reaction("<:lmao:758747233075200000>")
            return
        if 'lmao' in message.content.lower():
            await message.add_reaction("<:lmao:758747233075200000>")
            return
        if random.randint(0, 100) > 97 and not ('https://' in message.content or len(message.attachments) > 0):
            await message.add_reaction(random.choice(emojis))
        if random.randint(0,100) > 94 and message.author == self.bot.get_user(688872433842782293):
            await message.add_reaction("😻")
        if message.reference != None:
            messageid = message.reference.message_id
            referenced = await message.channel.fetch_message(messageid)
            if 'based' in message.content.lower():
                await referenced.add_reaction('<:based:764140006640975922>')
            if 'so true' in message.content.lower():
                await referenced.add_reaction('<:sotrue:825473477837848598>')
                
    @commands.Cog.listener()
    async def on_message_edit(self, old, message):
        if (len(message.attachments) > 0 or 'https://' in message.content) and not (self.bot.get_emoji('<:upvote:776161705960931399>') in message.reactions):
            await message.add_reaction('<:upvote:776161705960931399>')
            await message.add_reaction('<:downvote:776162465842200617>')
        if message.reference != None:
            messageid = message.reference.message_id
            referenced = await message.channel.fetch_message(messageid)
            if 'so true' in message.content.lower():
                await referenced.add_reaction('<:sotrue:825473477837848598>')
            if 'based' in message.content.lower():
                await referenced.add_reaction('<:based:764140006640975922>')            



    # ----------------------------------------------------
    @commands.command()
    async def stank(self,ctx):
        await ctx.channel.send('lmao imagine not having a !stank command')
        
    @commands.command()
    async def dm(self,ctx, userid, *, message):    
        me = self.bot.get_user(577668867380477962)
        if ctx.author == me:
            userid = int(userid)
            user = self.bot.get_user(userid)
            await user.send(message)
            
    @commands.command()
    async def message(self,ctx, channelid, *, message):    
     me = self.bot.get_user(577668867380477962)
     if ctx.author == me:
        channelid = int(channelid)
        channel = self.bot.get_channel(channelid)
        await channel.send(message)
    

def setup(bot):
    bot.add_cog(Extra(bot))
