import discord


def handle_error(error_msg):
    embed = discord.Embed(
        title="Something went wrong!",
        description="Join [our server](https://discord.gg/QwXXNGNkeh) to report this issue.",
        color=0xFF0000,
    )
    embed2 = discord.Embed(
        title="Missing Permissions",
        description="If you have problems with missing permissions but you are the server owner, please go to server setting, create a new role, apply administrator permissions, and then add the role to yourself.",
        color=0x00EAFF
    )

    embeds = [embed, embed2]
    try:
        raise error_msg  # raise other errors so they aren't ignored
    except Exception as e:
        print(e)
        return [e, embeds]
