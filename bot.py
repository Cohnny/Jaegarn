import discord
import responses
from Classes import JokeHandler
from discord.ext import commands
from datetime import datetime

TOKEN = 'MTE3MjI4NTU2MDgwMzU1NzQzNg.Go5xI6.R2XXxSpEeY3LkIaNT-HhkRJ3Zs0bkyo1QiiTjM'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.type == discord.ChannelType.private:
        await send_message(message, message.content, is_private=True)
    else:
        await bot.process_commands(message)


@bot.command()
async def greet(ctx):
    greeting = "Hello, I am your friendly bot!"
    await ctx.send(greeting)


@bot.command()
async def joke(ctx):
    try:
        response = await JokeHandler.print_joke(ctx)
        await ctx.send(response)
    except Exception as e:
        print(e)


@bot.command()
async def time(ctx):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"The current date and time is: {current_time}")


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        destination = message.author if is_private else message.channel
        await destination.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    bot.run(TOKEN)
