# fun.py
import discord, random, asyncio
from discord.ext import commands
from discord import Member

import colorama
from colorama import Fore
from colorama import Style

emojis = ["😎", "😍", "😂", "🥶", "😱", "😳", "🤢", "🥱", "🤐", "🤯", "🤠", "💀", "🤏", "👀", "🌵", "⚡️", "💦", "🎉",
          "🥳", "😈", "🤡", "✅", "❌", "🤔", "🙄", "🥺", "🤧", "🆗", "💰", "🥰", "😜", "💪", "🤙", "👑", "✈️", "🇺🇸",
          "⛓", "🔪","😕","👺","🐸","💅","🤦‍♀️","💆‍♀️","🧏‍♀️","💁‍♀️","🤒","🤮","🤥","🤤","😬","😰","🤭","🤫","😓","🥺", "<:lip_biting_2:771376430566342716>", "<:sotrue:825473477837848598>", "<:lmao:758747233075200000>"]

def attachm(message):
    return (len(message.attachments) > 0 or 'https://' in message.content)

 
async def refEm(search, searchbar, message): 
    emote_ref = { # when adding an emote to the dictionary, remember to add it to the search list as well
        "based": ['<:based:764140006640975922>'],
        "so true": ['<:sotrue:825473477837848598>'],
        "sotrue": ['<:sotrue:825473477837848598>'],
        "lmao": ['<:lmao:758747233075200000>'],
        "bruh": ['🗿'],
        "sexy": ["<:lip_biting_2:771376430566342716>", "<:lip_biting:771375731787431956>", "<:NSFW:771375278626832394>"],
        "ahaha": ["<:lip_biting_2:771376430566342716>", "<:lip_biting:771375731787431956>", "<:NSFW:771375278626832394>"],
        "sad!": ["<:sad:827304544944783391>"],
        "mark": ["<:mark:827299997602545704>"]
    }
    react = emote_ref[search]
    if search in searchbar.content.lower():
        await asyncio.sleep(0.5)
        for emote in react:
            await message.add_reaction(emote)

search_list = ['based', 'so true','sotrue', 'lmao', 'bruh', 'sexy', 'ahaha','sad!','mark']
# when adding to the search list, remember to add it to the dictionary as well

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emotes = {
            "based": '<:based:764140006640975922>',
            "sotrue" : "<:sotrue:825473477837848598>",
            "lmao" : '<:lmao:758747233075200000>',
            "upvote" : '<:upvote:776161705960931399>',
            "downvote" :'<:downvote:776162465842200617>'
            }

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + Style.BRIGHT + 'fun.py is active' + Style.RESET_ALL)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if 'ugh fine' in message.content.lower():
            await message.reply('https://tenor.com/view/poggers-pogchamp-pog-meme-animation-gif-19294003')
            await message.add_reaction("🥺")
            await message.add_reaction("👉")
            await message.add_reaction("👈")
            return
        if 'ur mom' in message.content.lower():
            #await message.reply('https://tenor.com/view/urmom-your-mom-baldi-defaultdance-gif-19665250')
            #await message.add_reaction("<:lmao:758747233075200000>")
            return #disabled
        if random.randint(0,100) > 94 and message.author == self.bot.get_user(688872433842782293):
            await asyncio.sleep(0.5)
            await message.add_reaction("😻")
        if not attachm(message):
            if message.reference != None: # I wanted to make this more simple and just add the emotes as part of the function, but i can't await
                messageid = message.reference.message_id
                referenced = await message.channel.fetch_message(messageid)
                for search in search_list:
                    await refEm(search,message, referenced)
            else:
                for search in search_list[1:]:
                    await refEm(search, message, message)
                if random.randint(0, 100) > 97:
                    await message.add_reaction(random.choice(emojis))
        #if message.content.startswith("!"):
        #    await message.reply("MY PREFIX IS ? NOW. PLEASE USE ? INSTEAD OF ! FOR COMMANDS")


                
                
    @commands.Cog.listener()
    async def on_message_edit(self, old, message):
        if attachm(message) and not (self.bot.get_emoji(776161705960931399) in message.reactions):
            try:
                await message.add_reaction('<:upvote:776161705960931399>')
                await message.add_reaction('<:downvote:776162465842200617>')
            except Exception as e:
                print(e)
        if message.reference != None:
            messageid = message.reference.message_id
            referenced = await message.channel.fetch_message(messageid)
            for search in search_list:
                await refEm(search, message, referenced)
        else:
            for search in search_list[1:]:
                await refEm(search, message, message)



    # -----------------------------------------------------
    @commands.command()
    async def stank(self,ctx):
        await ctx.message.add_reaction("✅")
        await ctx.channel.send('lmao imagine not having a ?stank command')
    
    # TODO: organize this command and make it a nice looking embed
    @commands.command()
    async def info(self,ctx, member: Member=None):
        await ctx.message.add_reaction("✅")
        if member is None:
            member = ctx.author
        await ctx.channel.send(f'**__THIS COMMAND IS STILL IN BETA__** \n\naccount created: {member.created_at} \nserver joined: {member.joined_at} \nstatus: {member.activity}')
        
    @commands.command()
    async def dm(self,ctx, userid, *, message):    
        await ctx.message.add_reaction("✅")
        me = self.bot.get_user(577668867380477962)
        if ctx.author == me:
            userid = int(userid)
            user = self.bot.get_user(userid)
            await user.send(message)
            
    @commands.command()
    async def message(self,ctx, channelid, *, message):   
        await ctx.message.add_reaction("✅") 
        me = self.bot.get_user(577668867380477962)
        if ctx.author == me:
            channelid = int(channelid)
            channel = self.bot.get_channel(channelid)
            await channel.send(message)
        

    @commands.command(name='flip')
    async def flip(self, ctx):
        await ctx.message.add_reaction("✅")
        if random.choice([1, 2]) == 1:
            await ctx.reply("https://cdn.discordapp.com/attachments/840745532736667648/840745647657582592/heads.png")
            print("HEADS!!")
        else:
            await ctx.reply("https://cdn.discordapp.com/attachments/840745532736667648/840745647657582592/heads.png")
            print("TAILS!")

    

def setup(bot):
    bot.add_cog(Extra(bot))
