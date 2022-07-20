import discord


def handle_error(error_msg):
    embed = discord.Embed(
        title="Something went wrong!",
        description="Join [our server](https://discord.gg/QwXXNGNkeh) to report this issue.",
        color=0xFF0000,
    )
    embed2 = discord.Embed(
        title="Missing Permissions",
        description="If you have problems with missing permissions, place the \"Fansic\"role on the top of the roles you want. If this still doesn't work for you, join the server above.",
        color=0x00EAFF
    )

    embeds = [embed, embed2]
    try:
        raise error_msg  # raise other errors so they aren't ignored
    except Exception as e:
        print(e)
        return [e, embeds]
