import discord
from discord.ext import commands

TOKEN = 'XXXXXXXXXXXX'

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(pass_context=True)
async def joingame(context, *args):
    author = context.message.author
    await bot.say('{0.mention} just joined !'.format(author))



bot.run(TOKEN, bot=True)
client.run(TOKEN)

