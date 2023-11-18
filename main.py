import asyncio
import discord
import datetime as dt
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from dalle import Dalle
from chatGPT import chatGPT
import os
import giveaway as giveaway

#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

reactDict = {
    "🍟" : "Movie Night",
    "🤗" : "Chat Revive",
    "👾" : "Live Notification",
    "📢" : "General Announcement"
}

@bot.event
async def on_ready():
    print("Bot is Up and Ready")
    if not daily_giveaway.is_running():
        daily_giveaway.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)

@tasks.loop(hours=24)
async def daily_giveaway():
    giveaways = await giveaway.getGiveaways()
    channel = 1170495453809360966
    msg = discord.Embed(title='Giveaways')
    msg.description = giveaways[0]
    await bot.get_channel(channel).send(embed=msg)

# -----------------INSERT BOT COMMANDS HERE--------------------------
# -----Nomad's Commands-----
#run the dalle command to generate an image
@bot.tree.command(name = "dalle", description = "Give a prompt and let openAI generate an image")
@app_commands.describe(prompt = "What prompt would you like to generate?")
async def dalle(ctx: discord.Interaction, prompt: str):
    await ctx.response.send_message("Give us a few seconds to generate your image.")
    user = ctx.user.id
    owner = 1170448075647635601
    api = os.getenv("APIKey")
    print(api)
    data = Dalle.generate(Dalle, prompt, api)
    if (data == "ERROR CODE 1"):
        await ctx.channel.send(f"""
        <@{owner}> API Key is invalid. Please fix in code.
        """)
        return
    if (data == "ERROR CODE 2"):
        await ctx.channel.send(f"""
        <@{owner}> Your being rate limited or hard limit reached. Fix please
        """)
        return
    if (data == "ERROR CODE 3"):
        await ctx.channel.send(f"""
        <@{user}> The OpenAI site is having issues at the moment!
        Please come back later!
        """)
        return
    if (data == "ERROR CODE 4"):
        await ctx.channel.send(f"""
        <@{user}> The prompt given is against OpenAI terms of service and was rejected.
        Please stay within openAI terms of service
        """)
        return
    else:
        with open("temp/dalle.png", 'rb') as image_file:
            await ctx.channel.send(f"""
            <@{user}> here's your image for prompt: {prompt}
            """, file=discord.File(image_file, filename='dalle.png'))
        os.remove("temp/dalle.png")

#generate text from chatgpt from a prompt
@bot.tree.command(name = "chat", description = "Give a prompt and let openAI generate text")
@app_commands.describe(prompt = "What prompt would you like to generate?")
@app_commands.describe(size = "What size do you want your prompt to return")
async def dalle(ctx: discord.Interaction, prompt: str, size: int):
    await ctx.response.send_message("Give us a few seconds to generate your text.")
    user = ctx.user.id
    owner = 1170448075647635601
    api = os.getenv("APIKey")
    data = chatGPT.generate(chatGPT, prompt, size, api)
    if (data == "ERROR CODE 1"):
        await ctx.channel.send(f"""
        <@{owner}> API Key is invalid. Please fix in code.
        """)
        return
    if (data == "ERROR CODE 2"):
        await ctx.channel.send(f"""
        <@{owner}> Your being rate limited or hard limit reached. Fix please
        """)
        return
    if (data == "ERROR CODE 3"):
        await ctx.channel.send(f"""
        <@{user}> The OpenAI site is having issues at the moment!
        Please come back later!
        """)
        return
    if (data == "ERROR CODE 4"):
        await ctx.channel.send(f"""
        <@{user}> The prompt given is against OpenAI terms of service and was rejected.
        Please stay within openAI terms of service
        """)
        return
    else:
        await ctx.channel.send(f"""
        <@{user}> here's your text for prompt: {prompt} : {data}
        """)

@bot.tree.command(name = "verify", description = "Give the secret code and get verified")
@app_commands.describe(verify_code = "What is the code used to verify from the rules channel?")
async def verify(ctx: discord.Interaction, verify_code: str):
    user = ctx.user.id
    if (verify_code != "Nomad Newbie Verify"):
        ctx.channel.send(f"<@{user}> The Password you gave was incorrect. Please provide a passcode")
    else:
        role = discord.utils.get(ctx.guild.roles, name="Verified")
        await ctx.user.add_roles(role)
        await ctx.response.send_message(f"<@{user}> You are now verified!")

@bot.event
async def on_member_join(member):
    guild = member.guild
    allMembers = discord.utils.get(guild.voice_channels, id=1170608099560792095)
    realMembers = discord.utils.get(guild.voice_channels, id=1170605758921056369)
    botMembers = discord.utils.get(guild.voice_channels, id=1170605822414438411)

    realMembersCount = sum(1 for m in guild.members if not m.bot)
    await realMembers.edit(name=f'Real Members: {realMembersCount}')
    botMembersCount = sum(1 for m in guild.members if m.bot)
    await botMembers.edit(name=f'Bots: {botMembersCount}')
    TotalMembers = sum(1 for m in guild.members)
    await allMembers.edit(name=f'Total Members: {TotalMembers}')

@bot.event
async def on_member_remove(member):
    guild = member.guild
    allMembers = discord.utils.get(guild.voice_channels, id=1170608099560792095)
    realMembers = discord.utils.get(guild.voice_channels, id=1170605758921056369)
    botMembers = discord.utils.get(guild.voice_channels, id=1170605822414438411)

    realMembersCount = sum(1 for m in guild.members if not m.bot)
    await realMembers.edit(name=f'Real Members: {realMembersCount}')
    botMembersCount = sum(1 for m in guild.members if m.bot)
    await botMembers.edit(name=f'Bots: {botMembersCount}')
    TotalMembers = sum(1 for m in guild.members)
    await allMembers.edit(name=f'Total Members: {TotalMembers}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != 1170681146233847860:
        return
    if (str(payload.emoji) in reactDict):
        Role = discord.utils.get(payload.member.guild.roles, name=reactDict[str(payload.emoji)])
        await payload.member.add_roles(Role)
    return

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != 1170681146233847860:
        return
    member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
    if (str(payload.emoji) in reactDict):
        Role = discord.utils.get(member.guild.roles, name=reactDict[str(payload.emoji)])
        await member.remove_roles(Role)
    return

#load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BotToken')
# run the bot with the key
bot.run(KEY)