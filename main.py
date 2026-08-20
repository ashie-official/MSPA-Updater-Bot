import discord as disc
from discord.ext import commands
from discord import app_commands as apps


################################################################################################################################


from toolkit import tk_str, tk_datetime, tk_str, tk_io


################################################################################################################################

from typing import Literal
import os
from dotenv import load_dotenv

load_dotenv()
try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    OWNER_ID = int(os.environ["OWNER_ID"])
    TEST_SERVER_ID = int(os.environ["TEST_SERVER_ID"])
except KeyError as e:
    raise KeyError(f"Configuration error: missing environment variable {e}") from None


################################################################################################################################


bot_prefix = "@#"
bot_status = "I NEED HUMAN BLOOD"


################################################################################################################################


class SlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=bot_prefix,
            intents=disc.Intents.default(),
            activity=disc.CustomActivity(
                name = bot_status
            ),
            status="online",
            owner_id = OWNER_ID
            )

    # Loading all the cogs
    async def _load_cogs(self) -> int:
        """Helper to iterate and load all extension cogs in ./cogs."""
        cog_count = 0
        cogs_dir = "./cogs"

        if not os.path.exists(cogs_dir):
            os.makedirs(cogs_dir)
            return cog_count

        for filename in os.listdir(cogs_dir):
            if (
                filename.endswith(".py")
                and not filename.startswith("_")
                and filename != "COG_TEMPLATE.py"
            ):
                cog_name = filename[:-3]
                try:
                    await self.load_extension(f"cogs.{cog_name}")
                    cog_count += 1
                except Exception as e:
                    print(f"Failed to load cog '{cog_name}': {e}")
                    try:
                        owner = await self.fetch_user(OWNER_ID)
                        await owner.send(
                            f"Couldn't load `{cog_name}` cog!\n```{e}```"
                        )
                    except disc.HTTPException:
                        pass
        return cog_count

    # Loading all the cogs
    async def setup_hook(self) -> None:
        """Executes before the bot connects to Discord gateway."""
        

        # Register error handler
        self.tree.error(self.error_handler)

        # Loading cogs and syncing bot tree
        loaded_count = await self._load_cogs()
        print(f"Successfully loaded {tk_str.plural(loaded_count, 'cog')}.")

        # Test server
        # self.tree.copy_global_to(guild=test_guild)
        # await self.tree.sync(guild=test_guild)

        # Global deployment
        await self.tree.sync()

    async def error_handler(
        self, intx: disc.Interaction, error: apps.AppCommandError
    ) -> None:
        """
        Global error handler for slash commands and tree interactions.
        """

        if isinstance(error, apps.TransformerError):
            await tk_io.error(
                intx, f"Invalid option: Could not parse input `{error.value}`"
            )
            return

        await tk_io.error(intx, f"`{error}`", append_input=True)


bot = SlashBot()

@bot.event
async def on_ready():
    now = tk_datetime.now()

    print(f"Logged in as {bot.user} at {now.strftime('%I:%M %p')}!")

    owner = await bot.fetch_user(OWNER_ID)
    await owner.send(f"Started bot at {tk_datetime.timezone_str(now, 't')}!", silent=True)


################################################################################################################################


@bot.group(name="admin")
@commands.is_owner()
# @commands.dm_only()
async def admin(ctx: commands.Context):
    pass


@admin.command()
async def load(ctx: commands.Context, extension: str):
    try:
        await bot.load_extension(f"cogs.{extension}")
    except Exception as e:
        error_msg = f"Error loading {extension}: {e}"
        print(error_msg)
        await ctx.send(error_msg)
    else:
        try:
            await bot.tree.sync()

            await ctx.send(f"Loaded and synced cog: `{extension}`")
            print(f'Loaded and synced cog: "{extension}"')
        except Exception as sync_error:
            print(f"Failed to sync command tree: {sync_error}")
            await ctx.send(f"Loaded `{extension}`, but failed to sync slash commands.")


@admin.command()
async def unload(ctx: commands.Context, extension: str):
    try:
        await bot.unload_extension(f"cogs.{extension}")
    except Exception as e:
        error_msg = f"Error unloading {extension}: {e}"
        print(error_msg)
        await ctx.send(error_msg)
    else:
        await bot.tree.sync()

        await ctx.send(f"Unloaded and synced cog: `{extension}`")
        print(f'Unloaded and synced cog: "{extension}"')


@admin.command()
async def reload(ctx: commands.Context, extension: str):
    try:
        await bot.reload_extension(f"cogs.{extension}")
    except Exception as e:
        error_msg = f"Error reloading {extension}: {e}"
        print(error_msg)
        await ctx.send(error_msg)
    else:
        await bot.tree.sync()

        await ctx.send(f"Reloaded and synced cog: `{extension}`")
        print(f'Reloaded and synced cog: "{extension}"')


@admin.command()
async def synctree(ctx: commands.Context, mode: Literal["global", "clear"]):
    """Manually triggers tree synchronization."""

    if mode == "global":
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {tk_str.plural(len(synced),'command')} globally.")

    elif mode == "clear":
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        await ctx.send("Cleared global command cache.")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
