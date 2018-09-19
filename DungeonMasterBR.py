#!/usr/bin/python3

import random
from collections import deque
import discord
from discord.ext import commands

from Map import Generator
from Player import Player
from Inventory import Inventory
from Object import Weapon

TOKEN = 'NDQ2NjcyNTEzODYzMjU0MDI2.Dlh4Ww.6ELuz08umoDRbCcz8Tw7h4vgEos'

# client = discord.Client()
bot = commands.Bot(command_prefix='!')

game_started = False
player_list = dict()
map_tiles = []
gen = None
player_order = deque()


def create_player(name, discord_id, author):
    if discord_id not in player_list.keys():
        new_player = Player(name, discord_id, author)
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

    for player in player_list.keys():
        player_added = False
        while not player_added:
            rand_x = random.randrange(0, 100)
            rand_y = random.randrange(0, 100)
            # TODO: Check if players are close close to each other
            if map_tiles[rand_x][rand_y] == 'floor':
                map_tiles[rand_x][rand_y] = player_list[player].discord_id
                # Update player object in the dictionary
                player_list[player].set_position(rand_x, rand_y)
                player_added = True
    gen.replace_map(map_tiles)


def order_players():
    global player_order
    player_pool = player_list.keys()
    random.shuffle(player_pool)
    player_order = deque(player_pool)


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
    create_player(name, author.id, author)

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
    author_id = author.id
    if author in player_list.keys():
        # TODO: Check if there is an item near the player
        player = player_list[author_id]
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
    player_info = player_list[author.id]
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
    player_info = player_list[author.id]

    await bot.send_message(author, 'Health: {}/100\nArmor: {}\nStamina: {}/10'
                           .format(player_info.health, player_info.armor, player_info.stamina))


@bot.command(pass_context=True)
async def move(context, *args):
    global player_list
    author = context.message.author
    name = author.name
    player_info = player_list[author.id]
    if 0 < len(args) < 3:
        move_x = args[0]
        move_y = args[1]
        # Check stamina if it's possible to move
        if player_info.stamina >= move_x + move_y:
            # Move player if you can move there
            if map_tiles[move_x][move_y] == 'floor':
                player_info.move(move_x, move_y)
                await  bot.say('{0.mention just moved.}'.format(author))
            else:
                await bot.say('{0.mention} can\' move  there. Try again.'.format(author))
        else:
            await bot.say('{0.mention} not enough stamina.'.format(author))
    else:
        await bot.say('{0.mention} command is used inappropriately.'.format(author))


@bot.command(pass_context=True)
async def inventory(context, *args):
    author = context.message.author
    name = author.name
    player_info = player_list[author.id]
    inv = '\n'.join(str(s) for s in player_info.inventory.item_list).strip()
    if inv != '' and inv != '\n' and inv is not None:
        await bot.send_message(author, inv)
    else:
        await bot.send_message(author, 'You have no items.')


@bot.command(pass_context=True)
async def end_turn(context, *args):
    global player_order
    author = context.message.author
    player_order.rotate(1)
    next_player = player_list[player_order.index(0)].author
    await bot.say('{0.mention} turn ended.\n {0.mention} turn starts now.'.format(author, next_player))


async def attack(wpn_type, context, pos_x, pos_y):
    author = context.message.author
    player_info = player_list[author.id]
    distance_attack = player_info.inventory.item_dic[wpn_type].wpn_range
    if pos_x < distance_attack or pos_y < distance_attack:
        attack_pos = map_tiles[player_info.position_x + pos_x][player_info.position_y + pos_y]
        if isinstance(attack_pos, int):
            player_info.attack(player_list[attack_pos])
            await bot.say('{0.mention} landed an attack.'.format(author))
            await bot.send_message(player_list[attack_pos].author,
                                   'You got hit for {} damage.'.format(player_info.inventory.item_dic[wpn_type].damage))
        else:
            await bot.say('{0.mention} missed the attack!'.format(author))


@bot.command(pass_context=True)
async def melee(context, *args):
    wpn_type = 'melee'
    pos_x = args[0]
    pos_y = args[1]
    attack(wpn_type, context, pos_x, pos_y)


@bot.command(pass_context=True)
async def shoot(context, *args):
    wpn_type = 'long_range'
    pos_x = args[0]
    pos_y = args[1]
    attack(wpn_type, context, pos_x, pos_y)


bot.run(TOKEN, bot=True)
# client.run(TOKEN)
