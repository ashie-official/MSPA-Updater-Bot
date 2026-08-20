import discord as disc
from discord import app_commands as apps
from discord.ext import commands as cmds

################################################################################################################################


from toolkit import tk_io
from toolkit import tk_command_info

CMD_INFO = tk_command_info.CMD_INFO["SCHEDULE"]


################################################################################################################################


class SCHEDULE(
    cmds.GroupCog,
    group_name=CMD_INFO["GROUP_INFORMATION"]["name"],
    group_description=CMD_INFO["GROUP_INFORMATION"]["desc"],
):
    def __init__(self, bot: cmds.Bot):
        self.bot = bot

    ################################################################################################

    @apps.command(
        name=CMD_INFO["COMMAND"]["name"],
        description=CMD_INFO["COMMAND"]["desc"],
    )
    @apps.describe(arg=CMD_INFO["COMMAND"]["args"]["arg"])
    async def cmd(self, intx: disc.Interaction, arg) -> None:
        embed = tk_io.build_embed(
            intx, title=CMD_INFO["COMMAND"]["title"], body=CMD_INFO["COMMAND"]["body"]
        )
        await intx.response.send_message(embed=embed, ephemeral=True)


################################################################################################################################


async def setup(bot):
    await bot.add_cog(SCHEDULE(bot))
