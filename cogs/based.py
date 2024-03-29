#based.py
# i promise im actually trying to be organized and not a complete mess i promise
import discord,time,random
from discord.ext import commands
from discord import Member
import sys, os.path

import firebase_admin
from firebase_admin import db
firebase_admin.get_app()
all_data = db.reference('/')

import colorama
from colorama import Fore
from colorama import Style

# TODO: SET UP A STORE FUNCTION. POSSIBLE BUYING OPTIONS: MUTE SOMEONE FOR 5 MINUTES, BOT FEATURE REQUEST

class Based(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.YELLOW + Style.BRIGHT + 'based.py is active'+ Style.RESET_ALL)
        
    # ------------- Leaderboard -----------------------------
        
    @commands.command(name='based')
    async def based(self,ctx, server_track="no id"):
        await ctx.message.add_reaction("✅")
        if server_track == "no id":
            server_track = ctx.guild
        else:
            server_track = self.bot.get_guild(int(server_track))
        id_ = ctx.author.id
        basedCount = all_data.child('basedcount').get()
        #basedCount = firebase.get('/' + FIREBASE_NAME + '/basedcount/', '')
        based_leader = []
        countss = []
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        for based_users in basedCount.items():
            #await ctx.send(based_users)
            user, count = based_users
            thePerson = self.bot.get_user(int(user))
            if thePerson in server_track.members:
                lname = str(thePerson.name) + '#' + str(thePerson.discriminator) + ':' + str(count) + '\n'
                based_leader.append([count, lname])
        based_leader = sorted(based_leader)
        based_leader = based_leader[::-1]
        leaderboard = "```"
        for i in based_leader:
            leaderboard += i[1]
        ud = await ctx.send(leaderboard + '```')
        await ud.add_reaction(upvote)
        await ud.add_reaction(downvote)


    @commands.command(name='upvote')
    async def upvote(self, ctx, server_track="no id"):
        await ctx.message.add_reaction("✅")
        if server_track == "no id":
            server_track = ctx.guild
        else:
            server_track = self.bot.get_guild(int(server_track))
        id_ = ctx.author.id
        basedCount = all_data.child('upvotecount').get()
        #basedCount = firebase.get('/' + FIREBASE_NAME + '/upvotecount/', '')
        based_leader = []
        countss = []
        downvote = self.bot.get_emoji(776162465842200617)
        upvote = self.bot.get_emoji(776161705960931399)
        for based_users in basedCount.items():
            #await ctx.send(based_users)
            user, count = based_users
            thePerson = self.bot.get_user(int(user))
            if thePerson in server_track.members:
                lname = str(thePerson.name) + '#' + str(thePerson.discriminator) + ':' + str(count) + '\n'
                based_leader.append([count, lname])
        based_leader = sorted(based_leader)
        based_leader = based_leader[::-1]
        leaderboard = "```"
        for i in based_leader:
            leaderboard += i[1]
        bas = await ctx.send(leaderboard + '```')
        await bas.add_reaction(upvote)
        await bas.add_reaction(downvote)
    
        
    # ------------ Trades and Bartering ----------------------
    
    @commands.command(name="give", aliases=["giveu"])
    async def giveu(self, ctx, recip: discord.Member, amount=1):
        await ctx.message.add_reaction("✅")
        amount = int(amount)
        if amount < 0:
            await ctx.send("Sorry, you can't give negative upvotes???")
            return
        ctx_id = ctx.author.id
        r_id = recip.id
        
        ctx_database = all_data.child('upvotecount').child(str(ctx_id))
        r_database = all_data.child('upvotecount').child(str(r_id))
        
        upCountCTX = int(ctx_database.get())
        upCountR = int(r_database.get())
        #upCountCTX = int(firebase.get('/' + FIREBASE_NAME + '/upvotecount/' + str(ctx_id), ''))
        #upCountR = int(firebase.get('/' + FIREBASE_NAME + '/upvotecount/' + str(r_id), ''))
        if upCountCTX < amount:
            await ctx.send(f"You don't have enough upvotes. Lmao poor loser")
            return
        upCountCTX -= amount
        upCountR += amount
        UpUpdateCountCTX = ctx_database.update(upCountCTX)
        UpUpdateCountCTX = r_database.update(upCountR)
        #UpUpdateCountCTX = firebase.put('/' + FIREBASE_NAME + '/upvotecount', str(ctx_id), upCountCTX)
        #UpUpdateCountR = firebase.put('/' + FIREBASE_NAME + '/upvotecount', str(r_id), upCountR)
        await ctx.reply(f"Transferred ***{amount}*** upvotes into {recip.mention}'s balance. {ctx.author.mention}'s balance is now ***{upCountCTX}***")
        
    @commands.command(name="giveb")
    async def giveb(self, ctx, recip: discord.Member, amount=1):
        await ctx.message.add_reaction("✅")
        amount = int(amount)
        if amount < 0:
            await ctx.send("Sorry, you can't give negative baseds???")
            return
        ctx_id = ctx.author.id
        r_id = recip.id
        ctx_database = all_data.child('basedcount').child(str(ctx_id))
        r_database = all_data.child('basedcount').child(str(r_id))
        
        upCountCTX = int(ctx_database.get())
        upCountR = int(r_database.get())

        
        #upCountCTX = int(firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(ctx_id), ''))
        #upCountR = int(firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(r_id), ''))
        if upCountCTX < amount:
            await ctx.send(f"You don't have enough baseds. Lmao poor loser")
            return
        upCountCTX -= amount
        upCountR += amount
        UpUpdateCountCTX = ctx_database.update(upCountCTX)
        UpUpdateCountR = ctx_database.update(upCountR)
        #UpUpdateCountCTX = firebase.put('/' + FIREBASE_NAME + '/basedcount', str(ctx_id), upCountCTX)
        #UpUpdateCountR = firebase.put('/' + FIREBASE_NAME + '/basedcount', str(r_id), upCountR)
        await ctx.send(f"Transferred ***{amount}*** baseds into {recip.mention}'s balance. {ctx.author.mention}'s balance is now ***{upCountCTX}***")


def setup(bot):
    bot.add_cog(Based(bot))
