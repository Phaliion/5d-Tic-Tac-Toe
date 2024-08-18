# for future self...
# I over commented for a reason...
# PLEASE USE THE COMMENTSSS


from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from http import server
import time
import traceback 
from asyncore import loop
from concurrent.futures.process import _threads_wakeups
from operator import not_
from pydoc import describe
from re import L
from sqlite3 import connect
from this import d
from threading import currentThread, Event
from turtle import pen
from typing import ValuesView
from unittest import TestProgram
import discord
from discord.ext import commands, tasks
from discord import *
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import colorama
from colorama import Fore
from math import ceil
import sys,os,string
import asyncio
import random



########################################

client = commands.Bot(command_prefix=";")
client.remove_command('help')
DiscordComponents(client)

os.system('cls')

@client.event
async def on_ready():
    os.system('cls')
    print("Bot is ready (5d Tic Tac Toe)")
    await client.change_presence(activity=discord.Game(name=f'the best 3 player game | ;help | \nMultiserver functionality is working!⠀⠀ Add this bot to your server and play it!'))

###################################### DONT COPY OVER ^^^^^^^^ #####################################################

def format(ctx):
    global server_vars

    if type(server_vars[str(ctx.message.guild.id)]) == list: return server_vars[str(ctx.message.guild.id)]

    elif type(server_vars[str(ctx.message.guild.id)]) == str: return [server_vars[str(ctx.message.guild.id)]]

def find_id(ctx):
    global server_vars
    keys = list(server_vars.keys())
    #all_ids = []
    listt = []

    for x in keys:
        listt += [x.split(",")]
    i = 0
    for x in listt:
        if str(ctx.message.guild.id) in x:
            #all_ids = x
            return str(keys[i])
        i += 1
    return "no game found"

version = "version - 1.0.4" ##################################### VERSION ##########################################


@client.command()
async def vars(ctx): # for testing
    global server_lobbys
    await ctx.send(server_lobbys)

@client.command()
async def update_notes(ctx): # copy invis unicode: "⠀"
    embedVar = discord.Embed(title = "- Update Notes - ", description = f"{version}")
    embedVar.add_field(name = "-Multiserver Compatability Added:", value = "Bot can be used Across Servers, You can now create lobbys and play with other people in different servers! P.S. This is kinda in beta so it might be buggy. **Please send feedback**", inline = False)
    await ctx.send(embed=embedVar)

@client.command()
async def help(ctx, catagory = None):
    global server_vars
    if server_vars != {}:
        board = server_vars[str(ctx.message.guild.id)][0]
        player_names = server_vars[str(ctx.message.guild.id)][2]

    if catagory == None:
        embedVar = discord.Embed(title="- Help -", description = "This is a **3** player game.")
        embedVar.add_field(name=";stop_game", value="Starts vote to end game.")
        embedVar.add_field(name=";create <@member> <@member> <@member>", value="Creates a new game.")
        embedVar.add_field(name=";show_board", value="Shows board at the beginning of the game. **DO NOT USE** if in the middle of a game.")
        embedVar.add_field(name=";help stalemate", value="Stalemate help.")
        embedVar.add_field(name=";help lobby", value="Lobby help.")
        embedVar.add_field(name=";guide", value="Explains how this game works, what everything means, and how to play.")
        embedVar.add_field(name=";update_notes", value="Update/patch notes of latest update.")
        try:
            if board != []:
                embedVar.add_field(name="⠀", value = "⠀", inline = False)
                embedVar.add_field(name="Turn order", value=f"{player_names[0]} :x:, {player_names[1]} :o:, {player_names[2]} :small_red_triangle:", inline=False)
        except: pass
        await ctx.send(embed=embedVar)


    # stalemate help
    elif catagory.lower() == "stalemate":
        embedVar = discord.Embed(title="- Stalemate Help -", description = "This is a **3** player game.")
        file = discord.File(r"C:\Users\raymo\OneDrive\Desktop\coding\bots\5d Tic Tac Toe 2.0\stalemate_example.png", filename="stalemate_example.png")
        embedVar.set_image(url="attachment://stalemate_example.png")

        embedVar.add_field(name="Deternine stalemate:", value="*The image below is a stalemate.*\n**Explanation:**\nThe player has to play in the bottom right square, but if they did, they would stay in that board and the bottom right board would be completely filled.\nThis means they cannot play in any square and cannot advance to a new board.\n**This is a stalemate**", inline=False)
        embedVar.add_field(name="Stalemate Example:", value="⠀", inline=True)

        await ctx.send(embed = embedVar, file=file)

    elif catagory.lower() == "lobby":
        embedVar = discord.Embed(title="- Lobby Help -", description = "This is a **3** player game.")
        embedVar.add_field(name=";lobby", value="Shows lobby finder.")
        embedVar.add_field(name=";lobby create <description>", value="Creates a lobby with a given description (description can be blank).")
        embedVar.add_field(name=";lobby join <lobby_name>", value="Joins a lobby.**\"lobby_name\" is the name your see before the description.**")
        embedVar.add_field(name=";lobby leave", value="Leaves the lobby you are currently in.")
        embedVar.add_field(name=";lobby disband",value="Disbands your lobby, (deletes lobby).")
        await ctx.send(embed=embedVar)

#########################################################
# format:    board, board_wins, player_names, playerAndBoardNum, playerTurn, random_square_remember, center_fixed. end_voted, multiserverfix
server_vars = {}
# format:    [[server_ids], title, message/description, # of players in lobby, code(if private)... None = public, started?, player_names]
# vars:      [[server_ids], title,     description,        playerCount,          lobbyCode : None,                started,       player_names]
server_lobbys = []
# format:    guild_id : lobby_code
server_codes = {}

# format for {playerAndBoardNum}:    player's turn   ,   board number
#                                                          1  2  3
#                                                          4  5  6
#                                                          7  8  9


#@tasks.loop(seconds=0)
#async def loop():


@client.command()
async def stop_game(ctx):
    global server_vars
    if len(format(ctx)) <= 2:
        board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
    else:
        board = server_vars[str(ctx.message.guild.id)][0]
        player_names = server_vars[str(ctx.message.guild.id)][2]

    if board == []:
        embedVar = discord.Embed(title="There is no game in progress!")
        await ctx.send(embed = embedVar)
        return
    playing = False
    for players in player_names:
        user = await client.fetch_user(int(players))
        user = str(user.name)
        if str(ctx.message.author).split("#")[0] == user:
            playing = True
    
    if playing == False:
        embedVar = discord.Embed(title="You are not playing!")
        await ctx.send(embed = embedVar)
        return

    await end_game(ctx, True)

@client.event
async def places(ctx):
    global server_vars

    if len(format(ctx)) <= 2:
        board_wins = server_vars[server_vars[str(ctx.message.guild.id)][0]][1]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
    else:
        board_wins = server_vars[str(ctx.message.guild.id)][1]
        player_names = server_vars[str(ctx.message.guild.id)][2]

    user1 = await client.fetch_user(int(player_names[0]))
    user1 = str(user1.name)
    user2 = await client.fetch_user(int(player_names[1]))
    user2 = str(user2.name)
    user3 = await client.fetch_user(int(player_names[2]))
    user3 = str(user3.name)
    player_total_wins = {user1 : 0, user2 : 0, user3 : 0}
    # count up wins / show total wins / declare winner
    try:
        for board_win in board_wins.split(","):
                
            if list(board_win)[0] == "1":
                player_total_wins[user1] += 1
            elif list(board_win)[0] == "2":
                player_total_wins[user2] += 1
            elif list(board_win)[0] == "3":
                player_total_wins[user3] += 1

        embedWin = discord.Embed(title = "Player Positions.")

        val_list = sorted(list(player_total_wins.values()))

        def get_key(val):
            keys = []
            for key, value in player_total_wins.items():
                if val == value:
                    keys += [key]
            
            if len(keys) > 1:
                return keys
            else:
                return keys[0]

        key1 = get_key(val_list[0])
        key2 = get_key(val_list[1])
        key3 = get_key(val_list[2])

        if len(key1) > 1:
            if type(key2) == str: key2 = [key2]
            if len(key2) > 1:
                key2 = key1[1]
                del key1[1]
            if type(key3) == str: key3 = [key3]
            if len(key3) > 1:
                key3 = key1[1]
                del key1[1]
            key1 = key1[0]
        elif len(key2) > 1:
            if type(key3) == str: key3 = [key3]
            if len(key3) > 1:
                key3 = key2[1]
                del key2[1]
            key2 = key2[0]


        sortedDict = {key1: val_list[0], key2: val_list[1], key3: val_list[2]}

        embedWin.add_field(name = ":first_place:", value=f"{list(sortedDict.keys())[2]}, with {list(sortedDict.values())[2]} boards won.")
        embedWin.add_field(name = ":second_place:", value=f"{list(sortedDict.keys())[1]}, with {list(sortedDict.values())[1]} boards won.")
        embedWin.add_field(name = ":third_place:", value=f"{list(sortedDict.keys())[0]}, with {list(sortedDict.values())[0]} boards won.")

        embedWin.set_footer(text="GG, thanks for playing!")

        await ctx.send(embed = embedWin)
        if len(format(ctx)) <= 2:
            try: del server_vars[server_vars[str(ctx.message.guild.id)]]
            except: pass
            finally: del server_vars[str(ctx.message.guild.id)]
        else:
            try: del server_vars[str(ctx.message.guild.id)]
            except: pass


    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Showing the Scores. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Showing Scores**\n{traceback.format_exc()}```")


@client.event
async def end_game(ctx, force_end = False):
    global server_vars

    if len(format(ctx)) <= 2:
        board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        board_wins = server_vars[server_vars[str(ctx.message.guild.id)][0]][1]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
        playerAndBoardNum = server_vars[server_vars[str(ctx.message.guild.id)][0]][3]
        playerTurn = server_vars[server_vars[str(ctx.message.guild.id)][0]][4]
        random_square_remember = server_vars[server_vars[str(ctx.message.guild.id)][0]][5]
        end_voted = server_vars[server_vars[str(ctx.message.guild.id)][0]][7]
    else:
        board = server_vars[str(ctx.message.guild.id)][0]
        board_wins = server_vars[str(ctx.message.guild.id)][1]
        player_names = server_vars[str(ctx.message.guild.id)][2]
        playerAndBoardNum = server_vars[str(ctx.message.guild.id)][3]
        playerTurn = server_vars[str(ctx.message.guild.id)][4]
        random_square_remember = server_vars[str(ctx.message.guild.id)][5]
        end_voted = server_vars[str(ctx.message.guild.id)][7]

    # global loop
    try:
        if "949065478033252472" in player_names:
            if player_names[0] == "949065478033252472":
                players_vote = {player_names[0] : True, player_names[1] : False, player_names[2] : False}
            if player_names[1] == "949065478033252472":
                players_vote = {player_names[0] : False, player_names[1] : True, player_names[2] : False}
            if player_names[2] == "949065478033252472":
                players_vote = {player_names[0] : False, player_names[1] : False, player_names[2] : True}
            end_voted += ["949065478033252472"]
        else:
            players_vote = {player_names[0] : False, player_names[1] : False, player_names[2] : False}

        #loop.cancel()


        # checking if the game has been forceably ended
        if force_end == True:
            # verify game ending
            embedVar = discord.Embed(title = "End Vote Started.", description = f"**3** \"Yes\" votes needed to end.\n**{len(end_voted)} voted**")
            embedVar.add_field(name="Yes", value="Agree to end.", inline=True)
            embedVar.add_field(name="No", value="Do not end.", inline=True)
            msgS = await ctx.send(
                        content = " ",
                        embed = embedVar,
                        components = [
                            [Button(label="Yes", style=3, custom_id="yes", disabled=False), Button(label="No", style=4, custom_id="no", disabled=False)]])

            while True:
                interactionS = await client.wait_for("button_click", check = lambda i: 
                ( i.custom_id == "yes",i.custom_id == "no" ))

                vote = str(interactionS.raw_data).split("{")[-1].split(":")[1].split(",")[0].replace("'","").replace(" ","") # button custom_id
                
                not_playing = True
                for name in player_names:
                    user = await client.fetch_user(int(name))
                    user = str(user.name)
                    if str(interactionS.user.name) == user:
                        not_playing = False
                if not_playing == True:
                    await interactionS.send(content = "You are not playing!", ephemeral=True)
                    continue
                

                found = False
                for name in end_voted:
                    if str(interactionS.user.name) == name: # change author to whoevers turn it is
                        await interactionS.send(content = "You already Voted!", ephemeral=True)
                        found = True
                if found == False:                
                    await interactionS.send(content = "Vote has been registered.", ephemeral=True)
                    if vote == "yes":
                        players_vote[str(interactionS.user.name)] = True
                        end_voted.append(str(interactionS.user.name))

                    elif vote == "no":
                        players_vote[str(interactionS.user.name)] = False
                        end_voted.append(str(interactionS.user.name))

                    embedVar3 = discord.Embed(title = "End Vote Started.", description = f"**3** \"Yes\" votes needed to end.\n**{len(end_voted)} voted**")
                    embedVar3.add_field(name="Yes", value="Agree to end.", inline=True)
                    embedVar3.add_field(name="No", value="Do not end.", inline=True)

                    await msgS.edit(embed = embedVar3)

                else: continue

                yes_count = 0
                if len(end_voted) == 3: 
                    for x in list(players_vote.values()):
                        if x == True: yes_count += 1

                    if yes_count == 3: 
                        embedVar2 = discord.Embed(title = "Game ended.")
                        await ctx.send(embed = embedVar2)
                        await places(ctx)

                        break

                    else: 
                        embedVar2 = discord.Embed(title = "The game continues!")
                        await ctx.send(embed = embedVar2)
                        end_voted = []
                        await board_event(ctx)
                        return
    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Ending The Game. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Ending The Game**\n{traceback.format_exc()}```")

@client.event
async def move(ctx):
    global server_vars

    if len(format(ctx)) <= 2:
        board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
        playerAndBoardNum = server_vars[server_vars[str(ctx.message.guild.id)][0]][3]
        playerTurn = server_vars[server_vars[str(ctx.message.guild.id)][0]][4]
        random_square_remember = server_vars[server_vars[str(ctx.message.guild.id)][0]][5]
        end_voted = server_vars[server_vars[str(ctx.message.guild.id)][0]][7]
    else:
        board = server_vars[str(ctx.message.guild.id)][0]
        player_names = server_vars[str(ctx.message.guild.id)][2]
        playerAndBoardNum = server_vars[str(ctx.message.guild.id)][3]
        playerTurn = server_vars[str(ctx.message.guild.id)][4]
        random_square_remember = server_vars[str(ctx.message.guild.id)][5]
        end_voted = server_vars[str(ctx.message.guild.id)][7]

    try:
        playerTurn = player_names[int(playerAndBoardNum[0]) - 1]
        board_num = int(playerAndBoardNum[-1])
        tiles = list(board[board_num - 1])

        if tiles[0] != '0' and tiles[0] != '7': q = True
        else: q = False
        if tiles[1] != '0' and tiles[1] != '7': w = True
        else: w = False
        if tiles[2] != '0' and tiles[2] != '7': e = True
        else: e = False
        if tiles[3] != '0' and tiles[3] != '7': r = True
        else: r = False
        if tiles[4] != '0' and tiles[4] != '7': t = True
        else: t = False
        if tiles[5] != '0' and tiles[5] != '7': y = True
        else: y = False
        if tiles[6] != '0' and tiles[6] != '7': u = True
        else: u = False
        if tiles[7] != '0' and tiles[7] != '7': i = True
        else: i = False
        if tiles[8] != '0' and tiles[8] != '7': o = True
        else: o = False

        user = await client.fetch_user(int(playerTurn))
        user = str(user).split("#")[0]
        if user != "5d Tic Tac Toe":
            msg = await ctx.send(
                    content = " ",
                    components = [
                        [Button(label=" ", style=(int(q) + 1), custom_id="button1", disabled=q), Button(label=" ", style=(int(w) + 1), custom_id="button2", disabled=w), Button(label=" ", style=(int(e) + 1), custom_id="button3", disabled=e)],
                        [Button(label=" ", style=(int(r) + 1), custom_id="button4", disabled=r), Button(label=" ", style=(int(t) + 1), custom_id="button5", disabled=t), Button(label=" ", style=(int(y) + 1), custom_id="button6", disabled=y)],
                        [Button(label=" ", style=(int(u) + 1), custom_id="button7", disabled=u), Button(label=" ", style=(int(i) + 1), custom_id="button8", disabled=i), Button(label=" ", style=(int(o) + 1), custom_id="button9", disabled=o)]
                    ],
                )

        async def place_piece(square):
            #print(board)

            # not working rn
                #get_data(str(ctx.message.guild.id), "write")

            # sets changing variables
            if len(format(ctx)) > 2:
                # sets new board number
                random_square = False
                rand_square = 5
                if board[int(playerAndBoardNum[-1]) - 1][4] == "7" and int(square) == 5:
                    while rand_square == 5:
                        rand_square = random.randint(1,9)

                    playerAndBoardNum[-1] = str(rand_square)
                    rand_square = str(rand_square)
                    random_square_remember = rand_square
                    random_square = True
                else: 
                    random_square_remember = ''


                temp_var = list(board[int(playerAndBoardNum[-1]) - 1])
                temp_var[int(square) - 1] = playerAndBoardNum[0]

                if random_square == False:
                    board[int(playerAndBoardNum[-1]) - 1] = ''.join(temp_var)

                elif random_square == True and int(square) == 5:
                    temp_var = []
                    for x in range(0,9):
                        if list(board[x])[4] == "7":
                            temp_var = list(board[x])
                            temp_var[4] = playerAndBoardNum[0]
                            board[x] = ''.join(temp_var)

                # next player
                if int(playerAndBoardNum[0]) + 1 == 4: playerAndBoardNum[0] = "1"
                else:
                    playerAndBoardNum[0] = str(int(playerAndBoardNum[0]) + 1)

                if random_square == False:
                    square = str(square)
                    playerAndBoardNum[-1] = square

                playerTurn = player_names[int(playerAndBoardNum[0]) - 1]
                server_vars[str(ctx.message.guild.id)][0] = board
                server_vars[str(ctx.message.guild.id)][2] = player_names
                server_vars[str(ctx.message.guild.id)][3] = playerAndBoardNum
                server_vars[str(ctx.message.guild.id)][4] = playerTurn
                server_vars[str(ctx.message.guild.id)][5] = random_square_remember
                server_vars[str(ctx.message.guild.id)][7] = end_voted
                server_vars[str(ctx.message.guild.id)][8] = True

            if len(format(ctx)) > 2:
                await detect_win(ctx)
                await detect_game_over(ctx)
            else:
                @tasks.loop(seconds=0)
                async def loop2():
                    global server_vars
                    if server_vars[server_vars[str(ctx.message.guild.id)][0]][8] == True: 
                        await board_event(ctx)
                        loop2.cancel()
                loop2.start()

            #loop.cancel()

        async def do_move(interaction):
            
            if len(format(ctx)) <= 2:
                board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
                player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
                playerAndBoardNum = server_vars[server_vars[str(ctx.message.guild.id)][0]][3]
                playerTurn = server_vars[server_vars[str(ctx.message.guild.id)][0]][4]
                random_square_remember = server_vars[server_vars[str(ctx.message.guild.id)][0]][5]
                end_voted = server_vars[server_vars[str(ctx.message.guild.id)][0]][7]
            else:
                board = server_vars[str(ctx.message.guild.id)][0]
                player_names = server_vars[str(ctx.message.guild.id)][2]
                playerAndBoardNum = server_vars[str(ctx.message.guild.id)][3]
                playerTurn = server_vars[str(ctx.message.guild.id)][4]
                random_square_remember = server_vars[str(ctx.message.guild.id)][5]
                end_voted = server_vars[str(ctx.message.guild.id)][7]

            user = await client.fetch_user(int(playerTurn))
            user = str(user).split("#")[0]
            bot_square = "0"
            while bot_square == "0":
                bot_square = str(random.randint(1,9))
                if str(list(board[int(playerAndBoardNum[-1]) - 1])[int(bot_square) - 1]) != "0": 
                    bot_square = "0"
                
            if user == "5d Tic Tac Toe":
                square = bot_square

            else:
                square = int(str(interaction.raw_data).split("{")[-1].split(":")[1].split(",")[0].replace("'","").replace(" ","").replace("button","")) # button custom_id
            return square

        #square = ''
        @tasks.loop(seconds=0)
        async def loop():
            #global square
            """if len(format(ctx)) <= 2:
                playerTurn = server_vars[server_vars[str(ctx.message.guild.id)]][4]
            else:
                playerTurn = server_vars[str(ctx.message.guild.id)][4]"""

            user = await client.fetch_user(int(playerTurn))
            user = str(user).split("#")[0]
            if user != "5d Tic Tac Toe":
                interaction = await client.wait_for("button_click", check = lambda i: (
                    i.custom_id == "button1",i.custom_id == "button2",i.custom_id == "button3",
                    i.custom_id == "button4",i.custom_id == "button5",i.custom_id == "button6",
                    i.custom_id == "button7",i.custom_id == "button8",i.custom_id == "button9")
                    )
                #print(server_vars[str(interaction.guild_id)][1])
                if (str(interaction.guild_id) == str(ctx.message.guild.id)) or (server_vars[str(ctx.message.guild.id)][0] == str(interaction.guild_id)) or (str(ctx.message.guild.id) == server_vars[str(interaction.guild_id)][0]) or (str(ctx.message.guild.id) == server_vars[str(interaction.guild_id)][1]):
                    square = await do_move(interaction)
                    if user != "5d Tic Tac Toe" and (str(interaction.user.mention).replace("<@","").replace(">","") == playerTurn or user == "5d Tic Tac Toe"):
                        server_vars[str(ctx.message.guild.id)][8] = False
                        await place_piece(square)
                        loop.cancel()
                            
                    else:
                        try:
                            await interaction.send(content = "It is not your turn.", ephemeral=True)
                        except: pass
            else:
                square = await do_move(None)
                await place_piece(square)
                loop.cancel()

        loop.start()
        #loop.start()
    
    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Detecting Board Plays. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Showing Buttons/Playing**\n{traceback.format_exc()}```")


@client.command()
async def lobby(ctx, type = None, *, message = None): # creates lobby for other servers to find 
    global server_vars
    global server_lobbys
    global server_codes

    # checks to see if lobby already exists in server
    if type != "join":
        for x in server_lobbys:
            if x[0] == str(ctx.message.guild.id): 
                embedVar = discord.Embed(title = "**A lobby already exists for your server!**", description = f"*Code: {x[4]}*")
                await ctx.send(embed=embedVar)
                return
    else:
        for x in server_lobbys:
            for i in range(0,3):
                try:
                    if x[6][i] == str(ctx.author.id):
                        embedVar = discord.Embed(title = "**You are already in a lobby!**")
                        await ctx.send(embed=embedVar)
                        return
                except: pass

    if type == "create":
        mode = 'Public'
        embedVar = discord.Embed(title="Create a Lobby", description = "**Public or Private**")
        msg = await ctx.send(
            content = " ",
            embed=embedVar,
            components = [
                [Button(label="Public", style=1, custom_id="public", disabled=False), Button(label="Private", style=1, custom_id="private", disabled=False), Button(label="✖", style=4, custom_id="close", disabled=False)]
            ],
        )
        while True:
            try:
                interaction = await client.wait_for("button_click", timeout=30, check = lambda i: (
                    i.custom_id == "public",i.custom_id == "private",i.custom_id == "close")
                )
                clicked = str(interaction.raw_data).split("{")[-1].split(":")[1].split(",")[0].replace("'","").replace(" ","")
                
                if interaction.user == ctx.author:
                    if clicked == "close":
                        embedClosed = discord.Embed(title = "Lobby Creater Closed")
                        await msg.edit(
                            embed=embedClosed,
                                components = [
                                    [Button(label="Public", style=2, custom_id="public", disabled=True), Button(label="Private", style=2, custom_id="private", disabled=True), Button(label="✖", style=2, custom_id="close", disabled=True)]
                            ],
                        )
                        return

                    else:
                        if clicked == "public": 
                            mode = "Public"

                        elif clicked == "private":
                            mode = "Private"

                        embedVar = discord.Embed(title="Create a Lobby", description = "**Lobby Created**")

                        if mode == "Private":
                            while True:
                                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))  
                                if code not in list(server_codes.values()):
                                    break
                        else:
                            code = None
                        embedVar.add_field(name=f"**{ctx.author}**", value=message)

                        server_lobbys.append([[str(ctx.message.guild.id)], str(ctx.author), message, 1, code, False, {str(ctx.author.id): str(ctx.message.guild.id)}])
                        server_codes.update({str(ctx.message.guild.id):code})

                        await msg.edit(
                            embed=embedVar,
                                components = [
                                    [Button(label="Public", style=2, custom_id="public", disabled=True), Button(label="Private", style=2, custom_id="private", disabled=True), Button(label="✖", style=2, custom_id="close", disabled=True)]
                            ],
                        )
                        await interaction.send(f"**Your lobby code**\n{code}")
                        @tasks.loop(seconds=0)
                        async def loop(ctx):
                            don = False
                            for x in server_lobbys:
                                if str(ctx.message.guild.id) in x[0]:
                                    don = True
                            if don == False:
                                await board_event(ctx)
                                loop.cancel()
                        loop.start(ctx)
                        return

            
            except asyncio.TimeoutError:
                embedTimeout = discord.Embed(title = "Lobby Searcher Timed out")
                await msg.edit(
                    embed=embedTimeout,
                    components = [
                        [Button(label="Public", style=2, custom_id="public", disabled=True), Button(label="Private", style=2, custom_id="private", disabled=True), Button(label="✖", style=2, custom_id="close", disabled=True)]
                    ],
                )
                return



    elif type == None:
        in_game = [False,0]
        for x in server_lobbys:
            if str(ctx.author.id) in list(x[6].keys()):
                in_game[0] = True
                in_game[1] == x[3]
        if len(server_lobbys) < 10 and len(server_lobbys) != 0:
            pages = 1
        else:
            pages = ceil(len(server_lobbys) / 10)
        current_page = 1
        if pages == 0 :
            embedVar = discord.Embed(title = "Lobbys", description = "**No Lobbies**")
            await ctx.send(embed=embedVar)
            return
        else:
            embedVar = discord.Embed(title = "Lobbys", description = f"**Page {current_page}**")

        for x in server_lobbys[((current_page - 1) * 10):][:10]:
            name = x[1]
            if x[4] != None:
                embedVar.add_field(name=f"**{name}** | *Private* | {x[3]}/3", value=f"*{x[2]}*", inline=False)
            else:
                embedVar.add_field(name=f"**{name}** | {x[3]}/3", value=f"*{x[2]}*", inline=False)

        left = True
        if pages > 1: right = False
        else: right = True

        if in_game[0] == True: 
            embedVar.set_footer(text=f"In lobby, {in_game[1]}/3 people")

        msg = await ctx.send(
            content = " ",
            embed=embedVar,
            components = [
                [Button(label="⮜", style=1, custom_id="left", disabled=left), Button(label="⮞", style=1, custom_id="right", disabled=right), Button(label="✖", style=4, custom_id="close", disabled=False)]
            ],
        )
        
        while True:
            try:
                interaction = await client.wait_for("button_click", timeout=30, check = lambda i: (
                    i.custom_id == "left",i.custom_id == "right",i.custom_id == "close")
                )
                clicked = str(interaction.raw_data).split("{")[-1].split(":")[1].split(",")[0].replace("'","").replace(" ","")

                if interaction.user == ctx.author:
                    if clicked == "close":
                        embedClosed = discord.Embed(title = "Lobby Searcher Closed")
                        await msg.edit(
                            embed=embedClosed,
                                components = [
                                    [Button(label="⮜", style=2, custom_id="left", disabled=True), Button(label="⮞", style=2, custom_id="right", disabled=True), Button(label="✖", style=2, custom_id="close", disabled=True)]
                            ],
                        )
                        break

                    else:
                        if clicked == "left": current_page -= 1
                        elif clicked == "right": current_page += 1

                        if current_page == 1: left = True
                        else: left = False
                        if current_page == pages: right = True
                        else: right = False

                        embedVar = discord.Embed(title = "Lobbies", description=f"**Page {current_page}**")

                        for x in server_lobbys[((current_page - 1) * 10):][:10]:
                            name = x[1]
                            if x[4] != None:
                                embedVar.add_field(name=f"**{name}** | *Private* | {x[3]}/3", value=f"*{x[2]}*", inline=False)
                            else:
                                embedVar.add_field(name=f"**{name}** | {x[3]}/3", value=f"*{x[2]}*", inline=False)
                            
                        if in_game[0] == True: 
                            embedVar.set_footer(text=f"In lobby, {in_game[1]}/3 people")

                        await msg.edit(
                            embed=embedVar,
                                components = [
                                    [Button(label="⮜", style=1, custom_id="left", disabled=left), Button(label="⮞", style=1, custom_id="right", disabled=right), Button(label="✖", style=4, custom_id="close", disabled=False)]
                            ],
                        )


            except asyncio.TimeoutError:
                embedTimeout = discord.Embed(title = "Lobby Searcher Timed out")
                await msg.edit(
                    embed=embedTimeout,
                    components = [
                        [Button(label="⮜", style=2, custom_id="left", disabled=True), Button(label="⮞", style=2, custom_id="right", disabled=True), Button(label="✖", style=2, custom_id="close", disabled=True)]
                    ],
                )
                break

    elif type == "join":
        ii=0
        for x in server_lobbys:
            if x[1] == message:
                if x[4] != None:
                    embedVar = discord.Embed(title="**Please enter a code**",description="*Ex: message \"16AFK\" into chat*")
                    edit_this = await ctx.send(embed=embedVar)
                    
                    def check(m):
                        return m.author == ctx.author

                    try:
                        msg = await client.wait_for('message', timeout=30, check = check)
                        # await ctx.send(msg.content)
                    
                    except asyncio.TimeoutError:
                        embedVar = discord.Embed(title="**Lobby join timed out!**")
                        await edit_this.edit(embed=embedVar)
                        return

                if x[3] != 3:
                    x[3] += 1
                    x[6].update({str(ctx.author.id): str(ctx.message.guild.id)})
                    if str(ctx.message.guild.id) not in x[0]:
                        x[0] += [str(ctx.message.guild.id)]
                        
                    if x[3] == 3:
                        x[5] = True
                        # starts game
                        l = 0
                        server_vars.update({x[0][0]:[['000000000','000000000','000000000','000000000','000000000','000000000','000000000','000000000','123321132'], 
    '00,00,00,00,00,00,00,00,00', [list(x[6].keys())[0], list(x[6].keys())[1], list(x[6].keys())[2]], ['1','5'], list(x[6].keys())[0], '', False, [], False]})
                        
                        if len(x[0]) == 3:
                            server_vars.update({x[0][1]: [x[0][0],x[0][2]]})
                            server_vars.update({x[0][2]: [x[0][0],x[0][1]]})
                        else:
                            server_vars.update({x[0][1]: [x[0][0]]})
                        
                        #await ctx.send(f"```{server_vars}```")
                        del server_lobbys[ii]

                        for i in range(0,3):
                            user = await client.fetch_user(list(x[6].keys())[i])
                            if (i == 0):
                                embedVar = discord.Embed(title = "**Your 5d Tic Tac Toe game has started!**",description="**If the board does not show up in your server, type \";show_board\"**")
                            else:
                                embedVar = discord.Embed(title = "**Your 5d Tic Tac Toe game has started!**",description="**If the board does not show up in your server, type \";show_board\"**")
                            await user.send(embed = embedVar)

                    embedVar = discord.Embed(title = f"**Joined \"{message}'s\" lobby!**")
                    await ctx.send(embed=embedVar)

                    #await ctx.send(x)
                    return
                else:
                    embedVar = discord.Embed(title="**This lobby is full!**")
                    await ctx.send(embed=embedVar)

                return
            ii += 1
        embedVar = discord.Embed(title="**Game not found!**",description = "*Be sure to put in the players name and tag (Bob#5932) when joining*")
        await ctx.send(embed=embedVar)

    elif type == "leave":
        for x in server_lobbys:
            if str(ctx.author.id) in list(x[6].keys()):
                if str(ctx.author.id) == list(x[6].keys())[0]:
                    embedVar = discord.Embed(title="**You cannot leave a party that you are hosting!**", description = "*Type \";lobby disband\" to disband the lobby*")
                    await ctx.send(embed=embedVar)
                    return
                else:
                    def get_value(ke):
                        values = []
                        for key, value in x[6].items():
                            if ke == key:
                                values += [value]
                        
                        if len(values) > 1:
                            return values
                        else:
                            return values[0]
                            
                    value = get_value(str(ctx.author.id))
                    x[6].pop(str(ctx.author.id))
                    if value not in list(x[6].values()):
                        x[0].remove(value)
                    x[3] -= 1
                    embedVar = discord.Embed(title = "**Left lobby**")
                    await ctx.send(embed=embedVar)
                    return

    elif type == "disband":
        i = 0
        for x in server_lobbys:
            if str(ctx.author.id) == list(x[6].keys())[0]:
                for l in list(x[6].keys()):
                    user = await client.fetch_user(int(l))
                    embedVar = discord.Embed(title="**Your 5d Tic Tac Toe lobby was disbanded!**", description = "*Don't look at me! I didn't do it...*")
                    await user.send(embed = embedVar)
                del server_lobbys[i]
                return
            else:
                embedVar = discord.Embed(title="**You cannot disband a game that you are not hosting!**", description = "*Type \";lobby leave\" to leave a party*")
                await ctx.send(embed=embedVar)
                return
            i += 1


@client.command()
async def create(ctx, member1 : discord.Member=None, member2 : discord.Member=None, member3 : discord.Member=None):
    global server_vars
    try:
        if len(format(ctx)) <= 2:
            board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        else:
            board = server_vars[str(ctx.message.guild.id)][0]
    except: 
        board = []
    if board != []: 
        embedVar = discord.Embed(title="There is a game already in progress!")
        await ctx.send(embed = embedVar)
        return

    if member1 == None or member2 == None or member3 == None:
        embedVar = discord.Embed(title="Please Input 3 Users... Ex: ;create @Bob @Billy @Tarry")
        await ctx.send(embed=embedVar)
        return

    # converts "Bob#2374" into "Bob" for all members
    member1, member2, member3 = str(member1.mention).replace("<@","").replace(">",""), str(member2.mention).replace("<@","").replace(">",""), str(member3.mention).replace("<@","").replace(">","")
    # check if game already exists in server
    for i in list(server_vars.keys()):
        if i == str(ctx.message.guild.id): # == True) means game does exist... == False) means does not exist
            embedVar = discord.Embed(title = "Game Already Exists")
            await ctx.send(embed=embedVar)
            return

    # creates and writes game to "server_vars"
    server_vars.update({str(ctx.message.guild.id):[['000000000','000000000','000000000','000000000','000000000','000000000','000000000','000000000','000000000'], 
    '00,00,00,00,00,00,00,00,00', [member1, member2, member3], ['1','5'], member1, '', False, [], False]})
    #if str(ctx.message.guild.id) == "806751868973482024":
    #    server_vars.update({"988591275680890901":str(ctx.message.guild.id)})

    
    await board_event(ctx)


##############################################################################################

# looking at the board on command
@client.command()
async def show_board(ctx):
    global server_vars

    if str(ctx.message.guild.id) not in list(server_vars.keys()):
        embedVar = discord.Embed(title = "**You are not in a game!**", description = "*Cannot show a board if you are not in a game*")
        await ctx.send(embed=embedVar)
        return

    if len(format(ctx)) <= 2:
        board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
    else:
        board = server_vars[str(ctx.message.guild.id)][0]
        player_names = server_vars[str(ctx.message.guild.id)][2]

    if board == []:
        embedVar = discord.Embed(title="There is no game in progress!")
        await ctx.send(embed = embedVar)
        return

    playing = False
    for players in player_names:
        user = await client.fetch_user(int(players))
        user = str(user.name)
        if str(ctx.message.author.name) == user:
            playing = True
    
    if playing == False:
        embedVar = discord.Embed(title="No disrupting their game!")
        await ctx.send(embed = embedVar)
        return

    #loop.cancel()
    await board_event(ctx)


@client.event
async def board_event(ctx):
    global server_vars
    # declare variables
    if len(format(ctx)) <= 2:
        board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        board_wins = server_vars[server_vars[str(ctx.message.guild.id)][0]][1]
        player_names = server_vars[server_vars[str(ctx.message.guild.id)][0]][2]
        playerAndBoardNum = server_vars[server_vars[str(ctx.message.guild.id)][0]][3]
        playerTurn = server_vars[server_vars[str(ctx.message.guild.id)][0]][4]
        random_square_remember = server_vars[server_vars[str(ctx.message.guild.id)][0]][5]
        center_fixed = server_vars[server_vars[str(ctx.message.guild.id)][0]][6]
        end_voted = server_vars[server_vars[str(ctx.message.guild.id)][0]][7]
    else:
        board = server_vars[str(ctx.message.guild.id)][0]
        board_wins = server_vars[str(ctx.message.guild.id)][1]
        player_names = server_vars[str(ctx.message.guild.id)][2]
        playerAndBoardNum = server_vars[str(ctx.message.guild.id)][3]
        playerTurn = server_vars[str(ctx.message.guild.id)][4]
        random_square_remember = server_vars[str(ctx.message.guild.id)][5]
        center_fixed = server_vars[str(ctx.message.guild.id)][6]
        end_voted = server_vars[str(ctx.message.guild.id)][7]


    # local vars
    boardNum = playerAndBoardNum[-1]
#              ↓↓↓↓↓↓↓↓↓↓ for bypassing char limit
    new_board, new_board2 = "", ""
    specific_tile = ""
    rearranged_board = ""
    specific_board = ""
    tile_decode = ""
    temp_board = board
    new_board = ""
    win_id = ""
    player_win = ""
    # for message split-off
    count = 0
    # detect stalemate
    stalemate = True
    try:
        for x in range(0,9):
            if list(board[int(playerAndBoardNum[-1]) - 1])[x] == "0":
                stalemate = False

        if stalemate == True:
            embedSt = discord.Embed(title = "Autodetected Stalemate!", description = "*If you think this is an error, message me your full board \"Phaliion#3642\"*\n**Go to \";help stalemate\" to learn how to prevent this.**")
            await ctx.send(embed=embedSt)
            
            await places(ctx)
            return

        # detect center filled
        center_filled = True
        for x in range(0,9):
            if list(board[4])[x] == "0":
                center_filled = False
        
        if center_filled == True:
            for x in range(0,9):
                if list(board[x])[4] == "0":
                    temp_board = []
                    temp_board = list(board[x])
                    temp_board[4] = "7"
                    board[x] = ''.join(temp_board)
                    center_fixed = True

        rand_filled = True
        if random_square_remember != "":
            for x in range(0,9):
                if list(board[int(random_square_remember) - 1])[x] == "0":
                    rand_filled = False


            if rand_filled == True:
                for x in range(0,9):
                    if list(board[x])[int(random_square_remember) - 1] == "0":
                        temp_board = []
                        temp_board = list(board[x])
                        temp_board[int(random_square_remember) - 1] = "8"
                        board[x] = ''.join(temp_board)
                        center_fixed = True
        

        temp_board = board
        # puts wins in board
        for i in range(0,9):
            player_win = list(board_wins.split(",")[i])[0]
            win_id = list(board_wins.split(",")[i])[-1]
            if win_id == "1":
                if player_win == "1":
                    new_board += "444"
                elif player_win == "2":
                    new_board += "555"
                elif player_win == "3":
                    new_board += "666"

                new_board += ''.join(list(board[i])[3:])

            elif win_id == "2":
                new_board += ''.join(list(board[i])[:3])

                if player_win == "1":
                    new_board += "444"
                elif player_win == "2":
                    new_board += "555"
                elif player_win == "3":
                    new_board += "666"

                new_board += ''.join(list(board[i])[6:])

            elif win_id == "3":
                new_board += ''.join(list(board[i])[:6])

                if player_win == "1":
                    new_board += "444"
                elif player_win == "2":
                    new_board += "555"
                elif player_win == "3":
                    new_board += "666"

            elif win_id == "4":
                for x in range(0,3):
                    if player_win == "1":
                        new_board += "4"
                    elif player_win == "2":
                        new_board += "5"
                    elif player_win == "3":
                        new_board += "6"
                    new_board += ''.join(list(board[i])[(x*3) + 1:][:2])

            elif win_id == "5":
                for x in range(0,3):
                    if x == 0: new_board += list(board[i])[0]

                    if player_win == "1":
                        new_board += "4"
                    elif player_win == "2":
                        new_board += "5"
                    elif player_win == "3":
                        new_board += "6"
                    new_board += ''.join(list(board[i])[(x*3) + 2:][:2])

            elif win_id == "6":
                for x in range(0,3):
                    if x == 0: new_board += ''.join(list(board[i])[0:2])

                    if player_win == "1":
                        new_board += "4"
                    elif player_win == "2":
                        new_board += "5"
                    elif player_win == "3":
                        new_board += "6"
                    new_board += ''.join(list(board[i])[(x*3) + 3:][:2])

            elif win_id == "7":
                for x in range(0,3):
                    if player_win == "1":
                        new_board += "4"
                    elif player_win == "2":
                        new_board += "5"
                    elif player_win == "3":
                        new_board += "6"
                    new_board += ''.join(list(board[i])[(x*4) + 1:][:3])

            elif win_id == "8":
                for x in range(0,3):
                    if x == 0: new_board += ''.join(list(board[i])[0:2])

                    if player_win == "1":
                        new_board += "4"
                    elif player_win == "2":
                        new_board += "5"
                    elif player_win == "3":
                        new_board += "6"
                    if x != 2: new_board += ''.join(list(board[i])[(x * 2) + 3])

                    if x == 2: new_board += ''.join(list(board[i])[7:])
            
            elif win_id == "0":
                new_board = temp_board[i]

            temp_board[i] = new_board
            new_board = ""

        # re-orders board so it's easily writeable
        for l in range(0,3):
            for i in range(0,3): # 00,00,00,00,00,00,00,00,00
                rearranged_board += ''.join(list(temp_board[(l * 3)])[(i * 3):][:3]) 
                rearranged_board += ''.join(list(temp_board[(l * 3) + 1])[(i * 3):][:3])
                rearranged_board += ''.join(list(temp_board[(l * 3) + 2])[(i * 3):][:3])

        # print(rearranged_board)

        # pick specific board
        for l in range(1,10):
            specific_board = ''.join(list(rearranged_board)[((l - 1) * 9):][:9])
            for i in range(0,9):
                specific_tile = list(specific_board)[i]

                if i == 3 or i == 6: 
                    # golden outline around board
                    if (boardNum == "1" and i == 3 and l >= 1 and l <= 3) or (boardNum == "2" and l >= 1 and l <= 3) or (boardNum == "3" and i == 6 and l >= 1 and l <= 3) or (boardNum == "4" and i == 3 and l >= 4 and l <= 6) or (boardNum == "5" and l >= 4 and l <= 6) or (boardNum == "6" and i == 6 and l >= 4 and l <= 6) or (boardNum == "7" and i == 3 and l >= 7 and l <= 9) or (boardNum == "8" and l >= 7 and l <= 9) or (boardNum == "9" and i == 6 and l >= 7 and l <= 9):
                        new_board2 += ":small_orange_diamond:"

                    else:    
                        new_board2 += ":black_large_square:"

                if specific_tile == "0":
                    tile_decode = ":black_square_button:"
                elif specific_tile == "1":
                    tile_decode = ":x:"
                elif specific_tile == "2":
                    tile_decode = ":o:"
                elif specific_tile == "3":
                    tile_decode = ":small_red_triangle:"

                elif specific_tile == "4":
                    tile_decode = ":regional_indicator_x:"
                elif specific_tile == "5":
                    tile_decode = ":regional_indicator_o:"
                elif specific_tile == "6":
                    tile_decode = ":arrow_up_small:"

                elif specific_tile == "7":
                    tile_decode = ":grey_question:"
                elif specific_tile == "8":
                    tile_decode = ":negative_squared_cross_mark:"

                count += 1
                new_board2 += tile_decode

            if count == 54:
                new_board = new_board2
                new_board2 = ""
            else:
                new_board2 += "\n"
                if count == 27 or count == 63:
                    for i in range(1,12):
                        if (((boardNum == "1" and count < 60) or boardNum == "4" or (boardNum == "7" and count > 60)) and i >= 1 and i <= 4) or (((boardNum == "2" and count < 60) or boardNum == "5" or (boardNum == "8" and count > 60)) and i >= 4 and i <= 8) or (((boardNum == "3" and count < 60) or boardNum == "6" or (boardNum == "9" and count > 60)) and i >= 8 and i <= 11 ):
                            new_board2 += ":small_orange_diamond:"
                        else:
                            new_board2 += ":black_large_square:"
                    new_board2 += "\n"
                    count += 9
            
        if int(playerAndBoardNum[0]) == 1: symbol = ":x:"
        elif int(playerAndBoardNum[0]) == 2: symbol = ":o:"
        elif int(playerAndBoardNum[0]) == 3: symbol = ":small_red_triangle:"

        user = await client.fetch_user(int(player_names[int(playerAndBoardNum[0]) - 1]))
        embedVar = discord.Embed(title = f"{user.name}'s Turn", description = symbol)
        await ctx.send(embed=embedVar)
        await ctx.send(new_board)
        await ctx.send(new_board2) 


        # sets changing variables
        if len(format(ctx)) > 2:
            server_vars[str(ctx.message.guild.id)][0] = board
            server_vars[str(ctx.message.guild.id)][1] = board_wins
            server_vars[str(ctx.message.guild.id)][2] = player_names
            server_vars[str(ctx.message.guild.id)][3] = playerAndBoardNum
            server_vars[str(ctx.message.guild.id)][4] = playerTurn
            server_vars[str(ctx.message.guild.id)][5] = random_square_remember
            server_vars[str(ctx.message.guild.id)][6] = center_fixed
            server_vars[str(ctx.message.guild.id)][7] = end_voted

        await move(ctx) 

    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Showing The Board. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Showing Board**\n{traceback.format_exc()}```")



#####################################################################
    
"""
id: 1
horizontal 1:     x  x  x
                  o  o  o
                  o  o  o
id: 2
horizontal 2 :    o  o  o
                  x  x  x
                  o  o  o
id: 3
horizontal 3:     o  o  o
                  o  o  o
                  x  x  x
id: 4
vertical 1 :      x  o  o
                  x  o  o
                  x  o  o
id: 5
vertical 2:       o  x  o
                  o  x  o
                  o  x  o
id: 6
vertical 3:       o  o  x
                  o  o  x
                  o  o  x
id: 7
diagnol 1:        x  o  o
                  o  x  o
                  o  o  x
id: 8
diagnol 2:        o  o  x
                  o  x  o
                  x  o  o
"""

@client.event
async def detect_game_over(ctx):
    global server_vars
    global server_lobbys
    try:
        if len(format(ctx)) <= 2:
            board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
        else:
            board = server_vars[str(ctx.message.guild.id)][0]

        game_not_over = False
        for miniboard in board:
            tiles = list(miniboard)
            for tile in tiles:
                if tile == "0":
                    game_not_over = True
        
        # game over
        if game_not_over == False:
            i = 0
            for x in server_lobbys:
                if str(ctx.message.guild.id) in x[0]:
                    del server_lobbys[i]
                    break
            i += 1

            await end_game(ctx)
        else:
            await board_event(ctx)

    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Detecting Game end. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Detecting Game Over**\n{traceback.format_exc()}```")



@client.event
async def detect_win(ctx):
    global server_vars
    try:
        if len(format(ctx)) <= 2:
            board = server_vars[server_vars[str(ctx.message.guild.id)][0]][0]
            board_wins = server_vars[server_vars[str(ctx.message.guild.id)][0]][1]
        else:
            board = server_vars[str(ctx.message.guild.id)][0]
            board_wins = server_vars[str(ctx.message.guild.id)][1]
        
        current_board = []
        new_board_wins = ''
        # for loop, for all 9 boards
        for i in range(0,9):
            if (board_wins.split(',')[i] == '00'):
                current_board = list(board[i]) # format:  "000 000 000"

    # horizontal 1
                if (''.join(current_board[0:][:3]) == '111') or (''.join(current_board[0:][:3]) == '222') or (''.join(current_board[0:][:3]) == '333'):
                    new_board_wins += current_board[0] + '1,'

    # horizontal 2
                elif (''.join(current_board[3:][:3]) == '111') or (''.join(current_board[3:][:3]) == '222') or (''.join(current_board[3:][:3]) == '333'):
                    new_board_wins += current_board[3] + '2,'

    # horizontal 3
                elif (''.join(current_board[6:][:3]) == '111') or (''.join(current_board[6:][:3]) == '222') or (''.join(current_board[6:][:3]) == '333'):
                    new_board_wins += current_board[6] + '3,'

    # vertical 1
                elif ((current_board[0] + current_board[3] + current_board[6]) == '111') or ((current_board[0] + current_board[3] + current_board[6]) == '222') or ((current_board[0] + current_board[3] + current_board[6]) == '333'):
                    new_board_wins += current_board[0] + '4,'

    # vertical 2
                elif ((current_board[1] + current_board[4] + current_board[7]) == '111') or ((current_board[1] + current_board[4] + current_board[7]) == '222') or ((current_board[1] + current_board[4] + current_board[7]) == '333'):
                    new_board_wins += current_board[1] + '5,'

    # vertical 3
                elif ((current_board[2] + current_board[5] + current_board[8]) == '111') or ((current_board[2] + current_board[5] + current_board[8]) == '222') or ((current_board[2] + current_board[5] + current_board[8]) == '333'):
                    new_board_wins += current_board[2] + '6,'

    # diagnol 1
                elif ((current_board[0] + current_board[4] + current_board[8]) == '111') or ((current_board[0] + current_board[4] + current_board[8]) == '222') or ((current_board[0] + current_board[4] + current_board[8]) == '333'):
                    new_board_wins += current_board[0] + '7,'

    # diagnol 2
                elif ((current_board[2] + current_board[4] + current_board[6]) == '111') or ((current_board[2] + current_board[4] + current_board[6]) == '222') or ((current_board[2] + current_board[4] + current_board[6]) == '333'):
                    new_board_wins += current_board[2] + '8,'

                else:
                    new_board_wins += '00,'

            else:
                new_board_wins += board_wins.split(',')[i] + ','

        # remove , at end of board_wins
        board_wins = new_board_wins[:-1]
        if len(format(ctx)) <= 2:
            server_vars[server_vars[str(ctx.message.guild.id)][0]][1] = board_wins
        else:
            server_vars[str(ctx.message.guild.id)][1] = board_wins

    except Exception as e:
        embedError = discord.Embed(title = "An Error has Accured Detecting Board Wins. This will be fixed ASAP, Sorry!", description = "Auto Contacted **Phaliion#3642** About Error...")
        await ctx.send(embed = embedError)

        # send error report
        user = await client.fetch_user(349177167416000514)
        await user.send(f"```**Error Detecting Board Wins**\n{traceback.format_exc()}```")

######################################################################



@client.command()
async def guide(ctx):
    embedVar = discord.Embed(title = 'Game Guide')

    embedVar.add_field(name = "Moving:", value = "Where you place your piece is where the next board will be. **e.g.** if you clicked in the top right square, it would go to the top right board.")
    embedVar.add_field(name = ":grey_question: square:", value = "When you place a piece in that square, it will give you that square and send you to a random board. \n*fixes starting in center phenomenon*", inline=False)
    embedVar.add_field(name="Try to avoid stalemate.", value="If you (bottom left) board is lookin like this:\n:x::o::small_red_triangle:\n:small_red_triangle::x::x:\n:black_square_button::o::small_red_triangle:\n Playing in the white square above will result in stalemate!\nTry to avoid stalemate by playing in the white square in the same position as the board.\n**Type \";help stalemate\" for more info**")
    
    embedVar.add_field(name="Which board are you on?", value = "The golden diamond outline around the board shows which board you are on.")
    
    await ctx.send(embed=embedVar)

client.run("", bot=True)