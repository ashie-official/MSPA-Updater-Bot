import discord as disc
from discord.ext import commands as cmds
from datetime import datetime, timezone

from typing import Any, Sequence, Optional
from discord import Embed, File, AllowedMentions
from discord.ui import View
from discord.utils import MISSING

################################################################################################################################

from toolkit import tk_datetime

################################################################################################################################


DATETIME_FORMAT_STR = "%Y-%m-%d %H:%M"


################################################################################################################################


def build_embed(
    intx: disc.Interaction,
    user: disc.User = None,  # type: ignore
    title: Optional[str] = None,
    body: Optional[str] = None,
    url: Optional[Any] = None,
    colour: Optional[disc.Colour] = None,
    ignore_footer=False,
) -> disc.Embed:

    if not user:
        user = intx.user

    embed = disc.Embed(
        title=title,
        description=body,
        url=url,
        timestamp=tk_datetime.now(),
        colour=colour,
    )

    if not ignore_footer:
        embed.set_footer(text="", icon_url=user.display_avatar.url)

    return embed


def _get_full_cmd_str(intx: disc.Interaction) -> str:
    if not intx.command:
        return ""
    return intx.command.qualified_name


async def error(intx: disc.Interaction, error_msg: str, append_input=True) -> None:
    embed = build_embed(
        intx=intx,
        title=":warning: ERROR! :warning:",
        body=error_msg,
        colour=disc.Colour.brand_red(),
    )

    if intx.command and append_input:
        cmd = _get_full_cmd_str(intx)
        lines = [f"`/{cmd}`"]

        args = vars(intx.namespace) if intx.namespace else {}
        if args:
            # lines.append('{')

            for k, v in args.items():
                lines.append(f"- `{k}`: {v}")

            # lines.append('}')

        embed.add_field(name="Input", value="\n".join(lines), inline=False)

        if args:
            args_strs = [f"{arg}: {value}" for arg, value in args.items()]

            embed.add_field(
                name="Raw Input",
                value=f"`/{cmd} {' '.join(args_strs)}`",
                inline=False,
            )

    await intx.response.send_message(intx, embed=embed, ephemeral=True)
