#!/usr/bin/python3

import random
import discord
from discord.ext import commands

from Map import Generator
from Player import Player
from Inventory import Inventory
from Object import Weapon

TOKEN = 'XXXXXXXXXXXXXX'

# client = discord.Client()
bot = commands.Bot(command_prefix='!')

game_started = False
player_list = dict()
map_tiles = []
gen = None


def create_player(name, discord_id):
    if discord_id not in player_list.keys():
        new_player = Player(name, discord_id)
        player_list[discord_id] = new_player


def delete_player(discord_id):
    del player_list[discord_id]


def create_map():
    # Create map
    global map_tiles
    global gen
    gen = Generator()
    map_tiles = gen.gen_level()


def add_players():
    # Add players to the map
    global player_list
    global map_tiles
    global gen
    number = 0

    for player in player_list.keys():
        player_added = False
        while not player_added:
            rand_x = random.randrange(0, 100)
            rand_y = random.randrange(0, 100)
            # TODO: Check if players are close close to each other
            if map_tiles[rand_x][rand_y] == 'floor':
                map_tiles[rand_x][rand_y] = number
                # Update player object in the dictionary
                updated_player = player_list[player]
                updated_player.set_position(rand_x, rand_y)
                player_list[player] = updated_player
                player_added = True
        number = number + 1
    gen.replace_map(map_tiles)


@bot.command(pass_context=True)
async def start_game(context):
    global game_started
    if not game_started:
        create_map()
        add_players()
        gen.gen_tiles_level()
        game_started = True
    else:
        await bot.say('A game is already in progress!')


@bot.command(pass_context=True)
async def end_game(context):
    global game_started
    game_started = False


@bot.command(pass_context=True)
async def join_game(context, *args):
    # Create and add a player to the board
    author = context.message.author
    name = author.name
    create_player(name, name + author.id)

    await bot.say('{0.mention} just joined !'.format(author))


@bot.command(pass_context=True)
async def sudoku(context, *args):
    # Commit sudoku
    author = context.message.author
    if author in player_list.keys():
        delete_player()
        await bot.say('{0.mention} just commited sudoku ):!'.format(author))


@bot.command(pass_context=True)
async def pickup(context, *args):
    author = context.message.author
    if author in player_list.keys():
        # TODO: Check if there is an item near the player
        player = player_list.get(author)
        if len(args) == 1:
            item = args[0]
            player.inventory.add_item(item)
            await bot.send_message(author, 'You successfully picked up {}.'.format(item))
            await bot.say('{0.mention} picked up an item.')
        elif len(args) == 2:
            item = args[0]
            slot = args[1]
            player.inventory.add_item(item, slot)
            await bot.send_message(author, 'You successfully added {} to your {} slot.'.format(item, slot))
            await bot.say('{0.mention} picked up an item'.format(author))
        else:
            await bot.say('{0.mention} please try again, more than two or no argument was passed.'.format(author))


@bot.command(pass_context=True)
async def look(context, *args):
    author = context.message.author
    name = author.name
    player_info = player_list[name + author.id]
    row = player_info.position_x
    column = player_info.position_y

    show = ''
    show += gen.tiles[map_tiles[row - 1][column - 1]]
    show += gen.tiles[map_tiles[row - 1][column]]
    show += gen.tiles[map_tiles[row - 1][column + 1]]
    show += '\n'
    show += gen.tiles[map_tiles[row][column - 1]]
    show += str(map_tiles[row][column])
    show += gen.tiles[map_tiles[row][column + 1]]
    show += '\n'
    show += gen.tiles[map_tiles[row + 1][column - 1]]
    show += gen.tiles[map_tiles[row + 1][column]]
    show += gen.tiles[map_tiles[row + 1][column + 1]]

    await bot.send_message(author, '' + show)


@bot.command(pass_context=True)
async def status(context, *args):
    author = context.message.author
    name = author.name
    player_info = player_list[name + author.id]

    await bot.send_message(author, 'Health: {}/100\nArmor: {}\nStamina: {}/10'
                           .format(player_info.health, player_info.armor, player_info.stamina))


@bot.command(pass_context=True)
async def move(context, *args):
    author = context.message.author
    name = author.name
    player_info = player_list[name + author.id]
    # Check stamina if it's possible to move
    move_x = 0
    move_y = 0

bot.run(TOKEN, bot=True)
# client.run(TOKEN)
