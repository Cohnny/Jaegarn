import discord
import responses
from Classes import JokeHandler


async def clear(ctx, amount: int):
    print(ctx)
    print(amount)
    if not amount:
        await ctx.send("Please provide a valid number of messages to clear.")
        return

    # Check if the user has permission to manage messages (adjust this as needed)
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
        await ctx.send(f"{amount} messages cleared by {ctx.author.mention}.", delete_after=5)
    else:
        await ctx.send("You don't have permission to manage messages.")


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_joke(message):
    try:
        response = await JokeHandler.print_joke(message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTE3MjI4NTU2MDgwMzU1NzQzNg.Go5xI6.R2XXxSpEeY3LkIaNT-HhkRJ3Zs0bkyo1QiiTjM'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        if user_message[0] == '!':
            if user_message.startswith('!clear'):  # Check if the message starts with "!clear"
                print("Inne i clear")
                user_message = user_message[len('!clear'):]  # Remove "!clear" from the message
            if user_message.strip():  # Check if there is a valid integer following the command
                print("Inne i strip")
                await clear(message, int(user_message.strip()))
            else:
                user_message = user_message[1:]
                if user_message == 'joke':
                    await send_joke(message)

    client.run(TOKEN)
