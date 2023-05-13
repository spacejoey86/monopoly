from board import Board
from player import Player
from APIKey import key

import disnake
from disnake.ext import commands
from typing import Callable, TypeVar, ParamSpec, Awaitable, Any

Context = commands.Context[commands.Bot]
T = TypeVar("T")
P = ParamSpec("P")

bot = commands.Bot(command_prefix=">", intents=disnake.Intents.all()) #alec said its fine tm

class DiscordBoard(Board):
    def __init__(self):
        super(DiscordBoard, self).__init__()
        self.current_players: set[int] = set()
        self.waiting_players: set[int] = set()
        self.leaving_players: set[int] = set()

games: dict[int, DiscordBoard] = {} #maps channel ID to a board (which is unique across guilds) and sets of players


def game_exists(f: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T|None]]:
    async def wrapper(*args: Any, **kwargs: Any) -> T|None:
        if len(args) == 0:
            raise TypeError("in_play only valid for bot commands")
        
        ctx = args[0]
        if not isinstance(ctx, commands.Context):
            raise TypeError("in_play only valid for bot commands")
        
        if ctx.channel.id not in games.keys():
            await ctx.reply("There isn't a game in this channel")
            return None
        return await f(*args, **kwargs)
    return wrapper

# def game_exists(func: Callable[P, Awaitable[None]]) -> Coroutine[P, Awaitable[None]]:
#     async def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
#         if len(args) == 0:
#             raise TypeError("in_play only valid for bot commands")
        
#         ctx = args[0]
#         if not isinstance(ctx, commands.Context):
#             raise TypeError("in_play only valid for bot commands")
        
#         if ctx.channel.id not in games.keys():
#             await ctx.reply("There isn't a game in this channel")
#             return
#         return await func(*args, **kwargs)
    
#     return wrapper


@bot.command(name="create")
async def create_handler(ctx: Context) -> None:
    if ctx.channel.id in games.keys():
        await ctx.reply("There is already a game in this channel")
    else:
        games[ctx.channel.id] = DiscordBoard()

@game_exists
@bot.command(name="join")
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