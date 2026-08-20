import discord as disc
from discord import app_commands as apps
from discord.ext import commands as cmds


################################################################################################################################


from toolkit.tk_command_info import CMD_INFO
from toolkit import tk_io


################################################################################################################################


class COG_NAME(
    cmds.GroupCog, 
    group_name=CMD_INFO['COG_NAME']['GROUP_INFORMATION']['name'], 
    group_description=CMD_INFO['COG_NAME']['GROUP_INFORMATION']['desc']
):
    def __init__(self, bot: cmds.Bot):
        self.bot = bot
    
    ################################################################################################
    
    @apps.command(
        name=CMD_INFO['COG_NAME']['COMMAND']['name'],
        description=CMD_INFO['COG_NAME']['COMMAND']['desc'],
    )
    @apps.describe(
        arg = CMD_INFO['COG_NAME']['COMMAND']['args']['arg']
    )
    async def cmd(self, intx: disc.Interaction, arg) -> None:
        embed = tk_io.build_embed(
            intx,
            title = CMD_INFO['COG_NAME']['COMMAND']['title'],
            body = CMD_INFO['COG_NAME']['COMMAND']['body']
        )
        await intx.response.send_message(embed=embed, ephemeral=True)


################################################################################################################################


async def setup(bot):
    await bot.add_cog(COG_NAME(bot))