![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue)  ![github repo badge: Powered By](https://img.shields.io/badge/Powered%20By-Discord-181717?color=blue) ![github repo badge: Host](https://img.shields.io/badge/Host-Heroku-181717?color=purple) ![github repo badge: Database](https://img.shields.io/badge/Database-Firebase-181717?color=orange) ![github repo badge: Using](https://img.shields.io/badge/Using-FFMPEG-181717?color=green)
# MEE7
anti-mee6 bot... and MORE

Do you hate MEE6? Like, absolutely despise MEE6? BOI SAME! Add me to your server for me to relentlessly mock the bastard whenever it speaks. Use !insult to build my arsenal. Together, we can do this 💪


Add me with the link: <http://tiny.cc/MEE7>

### Summary

A new moderation discord bot inspired by user dislike for a different moderation bot -- MEE6. Using a Firebase database MEE7 collected insults directed at MEE6 and used them to reply to MEE6's messages.

However, it developed more practically with moderation features such as muting, kicking, banning, and deleting messages. In addition, it uses FFMPEG functionality to edit and caption videos via user recommendation.

Eventually, the codebase was used to provide niche functions required for specific purposes outside of MEE7's original scope. These include editing media of all sorts, including videos and images, as  well as an emote tracker system for "upvotes" and "based" reacts

Built with Python, FFMPEG, discord.py, Bash Script

# Commands 
<details>
<summary> Original Functionality </summary>

**?insult** <example insult>

Add your marvelous insults to my dastardly database! (anything you put after !insult will be added to a database containing all insults)

**?mock** <example mock>

What if you want me to mock MEE6 right here, right now. MEE6 hasn't spoken but damn are you mad!

**?count** <example count>

See how many despicable acts of mockery I have committed against the dreaded MEE6!
</details>
<details>
<summary> Administrative </summary>
MEE7's list of administrative commands

**?kick {@person}**
Kicks people

**?ban {@person}**
Bans people

**?clear {number}**
Deletes {number} of messages in channel

**?unban {user ID}**
in development

**?invite {user ID}**
in development

</details>
<details>
<summary> Media </summary>
MEE7 allows you to perform several operations on a user's provided media
Works for replies means you can reply to a message with an attachment/link and it will still work


**?caption {attachment}** <example caption>

Captions media. Works for replies

**?deepfry {number} {attachment}** <example deepfry>

applies a deepfry filter onto provided media {number} times. Works for replies

**?download {link}** <example download>

Downloads a video from a link (reddit/youtube/etc) and sends it in a reply. Works for replies

**?speed {link/attachment}** <example speed>

Increases or Decreases the speed of a video (ex: 2x speed). Works for replies

**?convert {link/attachment}** <example convert>

Converts a video/link to an MP4 attachment. Works for replies

</details>
<details>
<summary> Barter System</summary>
MEE7 tracks all of your baseds and upvotes across every server that it is on. reply to someone with 'based' to increase their count, and react with the based and upvote reactions. While still in development, MEE7 is planned to allow users to buy features from MEE7 with these currencies


**?upvote**
Sends leaderboard of all upvotes

**?based**
Sends leaderboard of all baseds

**?give {@person} {number}**
Gives {@person} {number} more upvotes

**?giveb {@person} {number}**
Gives {@person} {number} more baseds

**MORE COMING SOON!**
in development
</details>