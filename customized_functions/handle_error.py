import discord


def handle_error(error_msg):
    embed = discord.Embed(
        title="Something went wrong!",
        description="Join [our server](https://discord.gg/QwXXNGNkeh) to report this issue.",
        color=0xFF0000,
    )
    try:
        raise error_msg  # raise other errors so they aren't ignored
    except Exception as e:
        print(e)
        return [e, embed]
