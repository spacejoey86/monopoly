from board import Board
from player import Player
from APIKey import key

import disnake
from disnake.ext import commands
from typing import Callable, TypeVar, ParamSpec, Any

Context = commands.Context[commands.Bot]
T = TypeVar("T")
P = ParamSpec("P")

bot = commands.Bot(command_prefix=">", intents=disnake.Intents.all()) #alec said its fine tm

# class DiscordBoard(Board):
#     def __init__(self):
#         super(DiscordBoard, self).__init__()
#         self.current_players: set[int] = set()
#         self.waiting_players: set[int] = set()
#         self.leaving_players: set[int] = set()

class DiscordPlayer(Player):
    def __init__(self, *args: tuple[Any], **kwargs: tuple[Any]]):
        super(Player, self).__init__(*args, **kwargs)
        self.discord_id = 

games: dict[int, Board] = {} #maps channel ID to a board (which is unique across guilds) and sets of players


async def game_exists(ctx: Context) -> bool:
    if ctx.channel.id not in games.keys():
        await ctx.reply("There isn't a game in this channel")
        return False
    return True


@bot.command(name="create")
async def create_handler(ctx: Context) -> None:
    if ctx.channel.id in games.keys():
        await ctx.reply("There is already a game in this channel")
    else:
        games[ctx.channel.id] = Board()
        await ctx.reply(f"A new monopoly game has been started in this channel")


@bot.command(name="join")
@commands.check(game_exists)
async def join_handler(ctx: Context) -> None:
    board = games[ctx.channel.id]
    if ctx.author.id in board.current_players and board.started:
        await ctx.reply("You are already playing the current game")
    elif ctx.author.id in board.waiting_players or ctx.author.id in board.current_players:
        await ctx.reply("You will already be included in the next game")
    elif board.started:
        board.waiting_players.add(ctx.author.id)
        await ctx.reply("You have been added to the queue for the next game")
    else:
        board.current_players.add(ctx.author.id)
        await ctx.reply("You have been added to the queue for the next game")

b = Board()
b.add_player(Player("an", "Ship"))
b.start()
b.add_player(Player("alec", "Shoe"))

bot.run(key)