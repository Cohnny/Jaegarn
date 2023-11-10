from jokeapi import Jokes


async def print_joke(message):
    j = await Jokes()
    blacklist = ['racist']
    if message.channel.is_nsfw():
        blacklist.append("nsfw")
    joke = await j.get_joke(blacklist=blacklist)
    if joke["type"] == "single":
        msg = joke["joke"]
    else:
        msg = joke["setup"]
        msg += f"|| {joke['delivery']} ||"

    return msg

