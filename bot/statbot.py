# Google Sheets API Imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# Discord Imports
import discord
from discord import AllowedMentions
import logging


#Other Imports
from pprint import pprint
import time
import math
import os
import traceback

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
if SPREADSHEET_ID == None:
    f = open("spreadsheetid.txt", "r")
    SPREADSHEET_ID = f.readline().strip()
    f.close()

PLAYERS_RANGE = 'Players!A2:AQ'
LADDER_RANGE = 'Ladder!A2:C'
SEASON_RANGE = 'Season!A2'
PRIZES_RANGE = 'Season!A3'

STATS_LINK = 'https://docs.google.com/spreadsheets/d/' + SPREADSHEET_ID
STATS_VIEW = 'https://datastudio.google.com/reporting/4e25d626-273c-4b9c-95df-c683bd5e69e8'

STAT_BOT_TOKEN = os.getenv('STAT_BOT_TOKEN')
if STAT_BOT_TOKEN == None:
    f = open("bottoken.txt", "r")
    STAT_BOT_TOKEN = f.readline().strip()
    f.close()

class PlayerData:
    def __init__(self, data):
        # Set all empty values to N/A
        for i in range(len(data)):
            if not data[i]:
                data[i] = "N/A"

        self.name = data[0] if 0 < len(data) else "N/A"
        self.role = data[1] if 1 < len(data) else "N/A"
        self.team = data[2] if 2 < len(data) else "N/A"
        self.wins_tot = data[3] if 3 < len(data) else "N/A"
        self.losses_tot = data[4] if 4 < len(data) else "N/A"
        self.win_rate = data[5] if 5 < len(data) else "N/A"
        self.time_played_tot = data[6] if 6 < len(data) else "N/A"
        self.time_played_avg = data[7] if 7 < len(data) else "N/A"
        self.kills_tot = data[8] if 8 < len(data) else "N/A"
        self.deaths_tot = data[9] if 9 < len(data) else "N/A"
        self.assists_tot = data[10] if 10 < len(data) else "N/A"
        self.kda_tot = data[11] if 11 < len(data) else "N/A"
        self.kill_participation = data[12] if 12 < len(data) else "N/A"
        self.kills_avg = data[13] if 13 < len(data) else "N/A"
        self.deaths_avg = data[14] if 14 < len(data) else "N/A"
        self.assists_avg = data[15] if 15 < len(data) else "N/A"
        self.kda_avg = data[16] if 16 < len(data) else "N/A"
        self.first_bloods = data[17] if 17 < len(data) else "N/A"
        self.first_bloods_pct = data[18] if 18 < len(data) else "N/A"
        self.largest_killing_spree = data[19] if 19 < len(data) else "N/A"
        self.largest_multi_kill = data[20] if 20 < len(data) else "N/A"
        self.gold_avg = data[21] if 21 < len(data) else "N/A"
        self.cs_avg = data[22] if 22 < len(data) else "N/A"
        self.cs_per_min_avg = data[23] if 23 < len(data) else "N/A"
        self.gold_share_avg = data[24] if 24 < len(data) else "N/A"
        self.dmg_avg = data[25] if 25 < len(data) else "N/A"
        self.dmg_per_min_avg = data[26] if 26 < len(data) else "N/A"
        self.dmg_share_avg = data[27] if 27 < len(data) else "N/A"
        self.dmg_taken_avg = data[28] if 28 < len(data) else "N/A"
        self.vision_score_avg = data[29] if 29 < len(data) else "N/A"
        self.vision_score_per_min_avg = data[30] if 30 < len(data) else "N/A"
        self.vision_wards_tot = data[31] if 31 < len(data) else "N/A"
        self.wards_placed_tot = data[32] if 32 < len(data) else "N/A"
        self.wards_killed_tot = data[33] if 33 < len(data) else "N/A"
        self.turret_kills = data[34] if 34 < len(data) else "N/A"
        self.dmg_to_turrets = data[35] if 35 < len(data) else "N/A"
        self.first_turret = data[36] if 36 < len(data) else "N/A"
        self.first_turret_pct = data[37] if 37 < len(data) else "N/A"
        self.rift_avg = data[38] if 38 < len(data) else "N/A"
        self.baron_avg = data[39] if 39 < len(data) else "N/A"
        self.dragon_avg = data[40] if 40 < len(data) else "N/A"
        self.fantasy_score = data[41] if 41 < len(data) else "N/A"
        self.elo = data[42] if 42 < len(data) else "N/A"

class SpreadSheet:

    def __init__(self):
        self.sheet = self.setupSheetsAPI()

    def setupSheetsAPI(self):
        print("Setting up connection to Google Sheets API...")

        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()

    def fetchPlayerData(self, name):
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=PLAYERS_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            for row in values:
                if "".join(row[0].split(" ")).lower() == "".join(name.split(" ")).lower():
                    return PlayerData(row)
        return None

    def fetchLadderData(self):
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=LADDER_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            return values
        return None

    def fetchPrizeData(self):
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=PRIZES_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            return values[0][0]
        return None

    def fetchSeasonData(self):
        #get's data from google sheets
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=SEASON_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            return values[0][0]
        return None

class MyClient(discord.Client):

    def __init__(self):
        super().__init__()
        self.sheet = SpreadSheet()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        logging.info('Got message "%s"', message)
        
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if client.user.mentioned_in(message):
            components = message.content.split()

            if str(self.user.id) in components[0]:
                await self.handleCommand(message, components[1:])
            else :
                await message.reply('Hello!', mention_author=True)

    async def on_error(event_name, *args, **kwargs):
        logging.warning(traceback.format_exc()) #logs the error

    async def ladder(self, message):
        data = self.sheet.fetchLadderData()

        header = "```{0:<5} {1:<32} {2:<6}```\n```".format("RANK","NAME","ELO")
        
        entriesPerPage = 10
        numPages = math.ceil(len(data) / entriesPerPage)
        maxIndex = numPages - 1

        def update(index):
            start = index * entriesPerPage
            end = start + entriesPerPage

            # pprint(data);
            entries = ["{0:<5} {1:<32} {2:<6}".format(str(row[0]) + ".", row[1], str(row[2])) if len(row) == 3 else "*****INVALID_DATA*****" for row in data[start:end]]
            content = header
            content += "\n".join(entries)
            content += "```"

            embed = discord.Embed(
                title="LeaderBoards",
                type="rich",
                description=content,
                colour=0xFFFF)
            embed.set_footer(text="page %d/%d" %(index + 1, numPages))
            return embed

        ladderMsg = await message.reply(embed=update(0))
        await ladderMsg.add_reaction('📌')
        await ladderMsg.add_reaction('⏮')
        await ladderMsg.add_reaction('◀')
        await ladderMsg.add_reaction('▶')
        await ladderMsg.add_reaction('⏭')
        await ladderMsg.add_reaction('🗑️')
        def check(reaction, user):
            return user == message.author and reaction.message == ladderMsg

        i = 0
        reaction = None
        delete = True
        while True:
            if str(reaction) == '📌':
                delete = False
                break;
            elif str(reaction) == '⏮':
                i = 0
                await ladderMsg.edit(embed = update(i))
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await ladderMsg.edit(embed = update(i))
            elif str(reaction) == '▶':
                if i < maxIndex:
                    i += 1
                    await ladderMsg.edit(embed = update(i))
            elif str(reaction) == '⏭':
                i = maxIndex
                await ladderMsg.edit(embed = update(i))
            elif str(reaction) == '🗑️':
                break
            try:
                reaction, user = await self.wait_for('reaction_add', timeout = 60.0, check = check)
                await ladderMsg.remove_reaction(reaction, user)
            except:
                break

        if delete:
            await ladderMsg.delete()
        else:
            await ladderMsg.clear_reactions()

    async def stats(self, message, name):
        if name == "":
            await message.reply('No Account specified', mention_author=True)
            return

        data = self.sheet.fetchPlayerData(name)
        if not data:
            await message.reply('No Stats Found For Player: %s' % name, mention_author=True)
            return

        page1 = discord.Embed (
            title = '%s\'s Stats' % data.name,
            description = 'Main Stats',
            colour = discord.Colour.orange()
        )

        # page1.add_field(name="Role", value=data.role, inline=True)
        # page1.add_field(name="Team", value=data.team, inline=True)
        page1.add_field(name="Games", value=data.losses_tot, inline=True)
        page1.add_field(name="Wins", value=data.wins_tot, inline=True)
        page1.add_field(name="Win %", value=data.win_rate, inline=True)
        page1.add_field(name="ELO", value=data.elo, inline=True)
        page1.add_field(name="KDA", value=data.kda_tot, inline=True)
        page1.add_field(name="AVG KDA", value=data.kda_avg, inline=True)
        page1.add_field(name="Kills", value=data.kills_tot, inline=True)
        page1.add_field(name="Deaths", value=data.deaths_tot, inline=True)
        page1.add_field(name="Assists", value=data.assists_tot, inline=True)
        page1.add_field(name="AVG Kills", value=data.kills_avg, inline=True)
        page1.add_field(name="AVG Deaths", value=data.deaths_avg, inline=True)
        page1.add_field(name="AVG Assists", value=data.assists_avg, inline=True)
        page1.add_field(name="First Bloods", value=data.first_bloods, inline=True)
        page1.add_field(name="FB%", value=data.first_bloods_pct, inline=True)
        page1.add_field(name="Fantasy Score", value=data.fantasy_score, inline=True)
        page1.set_footer(text="page 1/3")
        page2 = discord.Embed (
            title = '%s\'s Stats' % data.name,
            description = 'Stats Continued...',
            colour = discord.Colour.orange()
        )

        page2.add_field(name="Total Time played (mins)", value=data.time_played_tot, inline=True)
        page2.add_field(name="AVG Game Time (mins)", value=data.time_played_avg, inline=True)
        page2.add_field(name="AVG KP", value=data.kill_participation, inline=True)
        page2.add_field(name="Largest Killing Spree", value=data.largest_killing_spree, inline=True)
        page2.add_field(name="Largest Multi-Kill", value=data.largest_multi_kill, inline=True)
        page2.add_field(name="AVG Total Gold", value=data.gold_avg, inline=True)
        page2.add_field(name="AVG Minion CS", value=data.cs_avg, inline=True)
        page2.add_field(name="CS/M", value=data.cs_per_min_avg, inline=True)
        page2.add_field(name="AVG Gold Share", value=data.gold_share_avg, inline=True)
        page2.add_field(name="AVG Damage", value=data.dmg_avg, inline=True)
        page2.add_field(name="AVG DPM", value=data.dmg_per_min_avg, inline=True)
        page2.add_field(name="AVG D Share", value=data.dmg_share_avg, inline=True)
        page2.add_field(name="AVG Damage Taken", value=data.dmg_taken_avg, inline=True)
        page2.set_footer(text="page 2/3")
        page3 = discord.Embed (
            title = '%s\'s Stats' % data.name,
            description = 'Stats Continued...',
            colour = discord.Colour.orange()
        )

        page3.add_field(name="Vision Score", value=data.vision_score_avg, inline=True)
        page3.add_field(name="VS/M", value=data.vision_score_per_min_avg, inline=True)
        page3.add_field(name="Vision Wards", value=data.vision_wards_tot, inline=True)
        page3.add_field(name="Wards Placed", value=data.wards_placed_tot, inline=True)
        page3.add_field(name="Wards Killed", value=data.wards_killed_tot, inline=True)
        page3.add_field(name="Tower Kills", value=data.turret_kills, inline=True)
        page3.add_field(name="DMG to Turrets", value=data.dmg_to_turrets, inline=True)
        page3.add_field(name="First Tower", value=data.first_turret, inline=True)
        page3.add_field(name="First Tower %", value=data.first_turret_pct, inline=True)
        page3.add_field(name="AVG Rift Heralds", value=data.rift_avg, inline=True)
        page3.add_field(name="AVG Barons", value=data.baron_avg, inline=True)
        page3.add_field(name="AVG Dragons", value=data.dragon_avg, inline=True)
        
        page3.set_footer(text="page 3/3")
        pages = [page1, page2, page3]

        numPages = len(pages)
        maxIndex = numPages - 1


        statsMsg = await message.reply(embed = pages[0])
        await statsMsg.add_reaction('📌')
        await statsMsg.add_reaction('⏮')
        await statsMsg.add_reaction('◀')
        await statsMsg.add_reaction('▶')
        await statsMsg.add_reaction('⏭')
        await statsMsg.add_reaction('🗑️')
        def check(reaction, user):
            return user == message.author and reaction.message == statsMsg

        i = 0
        reaction = None
        delete = True
        while True:

            if str(reaction) == '📌':
                delete = False
                break;
            elif str(reaction) == '⏮':
                i = 0
                await statsMsg.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await statsMsg.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < maxIndex:
                    i += 1
                    await statsMsg.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = maxIndex
                await statsMsg.edit(embed = pages[i])
            elif str(reaction) == '🗑️':
                print("trashed")
                break

            try:
                reaction, user = await self.wait_for('reaction_add', timeout = 60.0, check = check)
                await statsMsg.remove_reaction(reaction, user)
            except:
                print("exceptions here")
                break

        if delete:
            await statsMsg.delete()
        else:
            await statsMsg.clear_reactions()
            

    async def synergy(self, message, components):
        await message.reply('synergy', mention_author=True)

    async def handleCommand(self, message, components):
        print(components)

        if components == []:
            await self.help(message)
            return
        
        command = components[0].lower()

        if command == 'ladder':
            await self.ladder(message)
        elif command == 'stats':
            name = " ".join(components[1:])
            await self.stats(message, name)
        elif command == 'synergy':
            await self.synergy(message)
        elif command == 'prizes':
            await self.prizes(message)
        elif command == 'season':
            await self.season(message)
        elif command == 'statsview' or command == 'stats_view':
            await message.reply(STATS_VIEW, mention_author=True)
        elif command == 'statslink' or command == 'stats_link':
            await message.reply(STATS_LINK, mention_author=True)
        elif command == 'help':
            await self.help(message)
        else:
            await message.reply("For a list of commands, please use: '%s help'" % self.user.mention, mention_author=True)
        
    async def prizes(self, message):
        data = self.sheet.fetchPrizeData()

        embed = discord.Embed (
            title = 'Prizes',
            description = data,
            colour = discord.Colour.red()
        )

        await message.reply(embed=embed, mention_author=True)


    async def season(self, message):
        data = self.sheet.fetchSeasonData()

        embed = discord.Embed (
            title = 'Current Season',
            description = data,
            colour = discord.Colour.red()
        )

        await message.reply(embed=embed, mention_author=True)


    async def help(self, message):

        # description ="""
        # *ladder* - displays the current ladder based on Fantasy Score
        # *stats <league_name>* - displays the stats of the specified user (You can copy paste by using @Orianna Bot profile)
        # *synergy* - under construction
        # *statsview* - view stats report on the web
        # *statslink* - view stats spreadsheet
        # """

        embed = discord.Embed (
            title = 'You Called For Help?',
            description = 'Usage is really easy, simply mention me with one of the following options!',
            colour = discord.Colour.red()
        )

        embed.add_field(name="ladder", value="displays the current ladder based on your local ELO", inline=False)
        embed.add_field(name="stats <league_name>", value="displays the stats of the specified user\n*Note: You can copy paste from `@Orianna Bot profile`*", inline=False)
        # embed.add_field(name="synergy", value="Under Construction", inline=False)
        embed.add_field(name="statsview", value="view stats report on the web", inline=False)
        embed.add_field(name="statslink", value="view stats spreadsheet", inline=False)
        embed.add_field(name="season", value="view current season", inline=False)
        embed.add_field(name="prizes", value="view prize list for current season", inline=False)

        await message.reply(embed=embed, mention_author=True)



    

client = MyClient()
client.run(STAT_BOT_TOKEN)




