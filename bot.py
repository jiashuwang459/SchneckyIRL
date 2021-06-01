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

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

f = open("spreadsheetid.txt", "r")
SPREADSHEET_ID = f.readline().strip();
f.close()

PLAYERS_RANGE = 'Players!A2:AP'
LADDER_RANGE = 'Ladder!A2:C'


STATS_LINK = 'https://docs.google.com/spreadsheets/d/' + SPREADSHEET_ID
STATS_VIEW = 'https://datastudio.google.com/u/0/reporting/1f7177c7-7e2c-447f-a075-b45f6c9dff4b/page/7YL4B?s=og4GydPyjQA'


f = open("bottoken.txt", "r")
SchneckyIRLBotToken = f.readline().strip();
f.close()


class PlayerData:
    def __init__(self, data):
        self.name = data[0] if data[0] else "N/A";
        self.role = data[1] if data[1] else "N/A";
        self.team = data[2] if data[2] else "N/A";
        self.wins_tot = data[3] if data[3] else "N/A";
        self.losses_tot = data[4] if data[4] else "N/A";
        self.win_rate = data[5] if data[5] else "N/A";
        self.time_played_tot = data[6] if data[6] else "N/A";
        self.time_played_avg = data[7] if data[7] else "N/A";
        self.kills_tot = data[8] if data[8] else "N/A";
        self.deaths_tot = data[9] if data[9] else "N/A";
        self.assists_tot = data[10] if data[10] else "N/A";
        self.kda_tot = data[11] if data[11] else "N/A";
        self.kill_participation = data[12] if data[12] else "N/A";
        self.kills_avg = data[13] if data[13] else "N/A";
        self.deaths_avg = data[14] if data[14] else "N/A";
        self.assists_avg = data[15] if data[15] else "N/A";
        self.kda_avg = data[16] if data[16] else "N/A";
        self.first_bloods = data[17] if data[17] else "N/A";
        self.first_bloods_pct = data[18] if data[18] else "N/A";
        self.largest_killing_spree = data[19] if data[19] else "N/A";
        self.largest_multi_kill = data[20] if data[20] else "N/A";
        self.gold_avg = data[21] if data[21] else "N/A";
        self.cs_avg = data[22] if data[22] else "N/A";
        self.cs_per_min_avg = data[23] if data[23] else "N/A";
        self.gold_share_avg = data[24] if data[24] else "N/A";
        self.dmg_avg = data[25] if data[25] else "N/A";
        self.dmg_per_min_avg = data[26] if data[26] else "N/A";
        self.dmg_share_avg = data[27] if data[27] else "N/A";
        self.dmg_taken_avg = data[28] if data[28] else "N/A";
        self.vision_score_avg = data[29] if data[29] else "N/A";
        self.vision_score_per_min_avg = data[30] if data[30] else "N/A";
        self.vision_wards_tot = data[31] if data[31] else "N/A";
        self.wards_placed_tot = data[32] if data[32] else "N/A";
        self.wards_killed_tot = data[33] if data[33] else "N/A";
        self.turret_kills = data[34] if data[34] else "N/A";
        self.dmg_to_turrets = data[35] if data[35] else "N/A";
        self.first_turret = data[36] if data[36] else "N/A";
        self.first_turret_pct = data[37] if data[37] else "N/A";
        self.rift_avg = data[38] if data[38] else "N/A";
        self.baron_avg = data[39] if data[39] else "N/A";
        self.dragon_avg = data[40] if data[40] else "N/A";
        self.fantasy_score = data[41] if data[41] else "N/A";


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
        #get's data from google sheets
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=PLAYERS_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            for row in values:
                if row[0] == name:
                    return PlayerData(row);
        return None;

    def fetchLadderData(self):
        #get's data from google sheets
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=LADDER_RANGE).execute()
        values = result.get('values', [])

        # pprint(values)
        if not values:
            if(DEBUG): print('No data found.')
        else:
            return values;
        return None;

class MyClient(discord.Client):

    def __init__(self):
        super().__init__()
        self.sheet = SpreadSheet();

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

    async def help(self, ctx):
        await ctx.reply('You Called For Help?', mention_author=True)

    async def ladder(self, message):
        await message.reply('ladder', mention_author=True)
        # data = self.sheet.fetchLadderData();

        # header = "```{0:<5} {1:<32} {2:<6}```\n```".format("RANK","NAME","POINTS")
        # entries = list();
        # rank = 1;

        # start = 0;
        # end = start + 10;

        # newData = data[start:end]

        # if newData == []:

        # entries = ["{0:<5} {1:<32} {2:<6}".format(str(row[0]) + ".", row[1], str(row[2])) for row in newData]
        # content = header
        # content += "\n".join(entries[:25]);
        # content += "```";



        # page1 = discord.Embed (
        #     title = 'Stats 1/3',
        #     description = 'Your Stats',
        #     colour = discord.Colour.orange()
        # )
        # page1.add_field(name="Role", value=data.role, inline=True)
        # page1.add_field(name="Team", value=data.team, inline=True)
        # page1.add_field(name="Wins", value=data.wins_tot, inline=True)
        # page1.add_field(name="Games", value=data.losses_tot, inline=True)
        # page1.add_field(name="Win %", value=data.win_rate, inline=True)
        # page1.add_field(name="Total Time played (mins)", value=data.time_played_tot, inline=True)
        # page1.add_field(name="AVE Game Time (mins)", value=data.time_played_avg, inline=True)
        # page1.add_field(name="Kills", value=data.kills_tot, inline=True)
        # page1.add_field(name="Deaths", value=data.deaths_tot, inline=True)
        # page1.add_field(name="Assists", value=data.assists_tot, inline=True)
        # page1.add_field(name="KDA", value=data.kda_tot, inline=True)
        # page1.add_field(name="AVE KP", value=data.kill_participation, inline=True)
        # page1.add_field(name="AVE K/G", value=data.kills_avg, inline=True)
        # page1.add_field(name="AVE D/G", value=data.deaths_avg, inline=True)
        # page1.add_field(name="AVE A/G", value=data.assists_avg, inline=True)
        # page1.add_field(name="AVE KDA/G", value=data.kda_avg, inline=True)
        # page1.add_field(name="First Bloods", value=data.first_bloods, inline=True)
        # page1.add_field(name="FB%", value=data.first_bloods_pct, inline=True)
        # page2 = discord.Embed (
        #     title = 'Stats 2/3',
        #     description = 'Your Stats',
        #     colour = discord.Colour.orange()
        # )
        # page2.add_field(name="Largest Killing Spree", value=data.largest_killing_spree, inline=True)
        # page2.add_field(name="Largest Multi-Kill", value=data.largest_multi_kill, inline=True)
        # page2.add_field(name="AVE Total Gold", value=data.gold_avg, inline=True)
        # page2.add_field(name="AVE Minion CS", value=data.cs_avg, inline=True)
        # page2.add_field(name="CS/M", value=data.cs_per_min_avg, inline=True)
        # page2.add_field(name="AVE Gold Share", value=data.gold_share_avg, inline=True)
        # page2.add_field(name="AVE Damage", value=data.dmg_avg, inline=True)
        # page2.add_field(name="AVE DPM", value=data.dmg_per_min_avg, inline=True)
        # page2.add_field(name="AVE D Share", value=data.dmg_share_avg, inline=True)
        # page2.add_field(name="AVE Damage Taken", value=data.dmg_taken_avg, inline=True)
        # page2.add_field(name="Vision Score", value=data.vision_score_avg, inline=True)
        # page2.add_field(name="VS/M", value=data.vision_score_per_min_avg, inline=True)
        # page2.add_field(name="Vision Wards", value=data.vision_wards_tot, inline=True)
        # page2.add_field(name="Wards Placed", value=data.wards_placed_tot, inline=True)
        # page2.add_field(name="Wards Killed", value=data.wards_killed_tot, inline=True)
        # page3 = discord.Embed (
        #     title = 'Stats 3/3',
        #     description = 'Your Stats',
        #     colour = discord.Colour.orange()
        # )
        # page3.add_field(name="Tower Kills", value=data.turret_kills, inline=True)
        # page3.add_field(name="DMG to Turrets", value=data.dmg_to_turrets, inline=True)
        # page3.add_field(name="First Tower", value=data.first_turret, inline=True)
        # page3.add_field(name="First Tower %", value=data.first_turret_pct, inline=True)
        # page3.add_field(name="AVE Rift Heralds", value=data.rift_avg, inline=True)
        # page3.add_field(name="AVE Barons", value=data.baron_avg, inline=True)
        # page3.add_field(name="AVE Dragons", value=data.dragon_avg, inline=True)
        # page3.add_field(name="Fantasy Score", value=data.fantasy_score, inline=True)
        # pages = [page1, page2, page3]


        # async def updateReactions(statsMsg):
        #     await statsMsg.clear_reactions()
        #     await statsMsg.add_reaction('⏮')
        #     await statsMsg.add_reaction('◀')
        #     await statsMsg.add_reaction('▶')
        #     await statsMsg.add_reaction('⏭')

        # statsMsg = await message.reply(embed = page1)
        # await updateReactions(statsMsg)

        # def check(reaction, user):
        #     return user == message.author

        # i = 0
        # reaction = None

        # while True:
        #     if str(reaction) == '⏮':
        #         i = 0
        #         await statsMsg.edit(embed = pages[i])
        #         await updateReactions(statsMsg)
        #     elif str(reaction) == '◀':
        #         if i > 0:
        #             i -= 1
        #             await statsMsg.edit(embed = pages[i])
        #             await updateReactions(statsMsg)
        #     elif str(reaction) == '▶':
        #         if i < 2:
        #             i += 1
        #             await statsMsg.edit(embed = pages[i])
        #             await updateReactions(statsMsg)
        #     elif str(reaction) == '⏭':
        #         i = 2
        #         await statsMsg.edit(embed = pages[i])
        #         await updateReactions(statsMsg)
        #     try:
        #         reaction, user = await self.wait_for('reaction_add', timeout = 30.0, check = check)
        #     except:
        #         break

        # await statsMsg.clear_reactions()

        
        await message.reply(embed=discord.Embed(
            title="LeaderBoards",
            type="rich",
            description=content,
            colour=0xFFFF))

    async def stats(self, message, components):
        if components == []:
            await message.reply('No Account specified', mention_author=True)
            return

        name = " ".join(components)

        data = self.sheet.fetchPlayerData(name);
        if not data:
            await message.reply('No Stats Found For Player: %s', name, mention_author=True)
            return

        page1 = discord.Embed (
            title = 'Stats 1/3',
            description = 'Your Stats',
            colour = discord.Colour.orange()
        )
        page1.add_field(name="Role", value=data.role, inline=True)
        page1.add_field(name="Team", value=data.team, inline=True)
        page1.add_field(name="Wins", value=data.wins_tot, inline=True)
        page1.add_field(name="Games", value=data.losses_tot, inline=True)
        page1.add_field(name="Win %", value=data.win_rate, inline=True)
        page1.add_field(name="Total Time played (mins)", value=data.time_played_tot, inline=True)
        page1.add_field(name="AVE Game Time (mins)", value=data.time_played_avg, inline=True)
        page1.add_field(name="Kills", value=data.kills_tot, inline=True)
        page1.add_field(name="Deaths", value=data.deaths_tot, inline=True)
        page1.add_field(name="Assists", value=data.assists_tot, inline=True)
        page1.add_field(name="KDA", value=data.kda_tot, inline=True)
        page1.add_field(name="AVE KP", value=data.kill_participation, inline=True)
        page1.add_field(name="AVE K/G", value=data.kills_avg, inline=True)
        page1.add_field(name="AVE D/G", value=data.deaths_avg, inline=True)
        page1.add_field(name="AVE A/G", value=data.assists_avg, inline=True)
        page1.add_field(name="AVE KDA/G", value=data.kda_avg, inline=True)
        page1.add_field(name="First Bloods", value=data.first_bloods, inline=True)
        page1.add_field(name="FB%", value=data.first_bloods_pct, inline=True)
        page2 = discord.Embed (
            title = 'Stats 2/3',
            description = 'Your Stats',
            colour = discord.Colour.orange()
        )
        page2.add_field(name="Largest Killing Spree", value=data.largest_killing_spree, inline=True)
        page2.add_field(name="Largest Multi-Kill", value=data.largest_multi_kill, inline=True)
        page2.add_field(name="AVE Total Gold", value=data.gold_avg, inline=True)
        page2.add_field(name="AVE Minion CS", value=data.cs_avg, inline=True)
        page2.add_field(name="CS/M", value=data.cs_per_min_avg, inline=True)
        page2.add_field(name="AVE Gold Share", value=data.gold_share_avg, inline=True)
        page2.add_field(name="AVE Damage", value=data.dmg_avg, inline=True)
        page2.add_field(name="AVE DPM", value=data.dmg_per_min_avg, inline=True)
        page2.add_field(name="AVE D Share", value=data.dmg_share_avg, inline=True)
        page2.add_field(name="AVE Damage Taken", value=data.dmg_taken_avg, inline=True)
        page2.add_field(name="Vision Score", value=data.vision_score_avg, inline=True)
        page2.add_field(name="VS/M", value=data.vision_score_per_min_avg, inline=True)
        page2.add_field(name="Vision Wards", value=data.vision_wards_tot, inline=True)
        page2.add_field(name="Wards Placed", value=data.wards_placed_tot, inline=True)
        page2.add_field(name="Wards Killed", value=data.wards_killed_tot, inline=True)
        page3 = discord.Embed (
            title = 'Stats 3/3',
            description = 'Your Stats',
            colour = discord.Colour.orange()
        )
        page3.add_field(name="Tower Kills", value=data.turret_kills, inline=True)
        page3.add_field(name="DMG to Turrets", value=data.dmg_to_turrets, inline=True)
        page3.add_field(name="First Tower", value=data.first_turret, inline=True)
        page3.add_field(name="First Tower %", value=data.first_turret_pct, inline=True)
        page3.add_field(name="AVE Rift Heralds", value=data.rift_avg, inline=True)
        page3.add_field(name="AVE Barons", value=data.baron_avg, inline=True)
        page3.add_field(name="AVE Dragons", value=data.dragon_avg, inline=True)
        page3.add_field(name="Fantasy Score", value=data.fantasy_score, inline=True)
        pages = [page1, page2, page3]


        async def updateReactions(statsMsg):
            await statsMsg.clear_reactions()
            await statsMsg.add_reaction('⏮')
            await statsMsg.add_reaction('◀')
            await statsMsg.add_reaction('▶')
            await statsMsg.add_reaction('⏭')
            await statsMsg.add_reaction('❌')

        statsMsg = await message.reply(embed = page1)
        await updateReactions(statsMsg)

        def check(reaction, user):
            return user == message.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await statsMsg.edit(embed = pages[i])
                await updateReactions(statsMsg)
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await statsMsg.edit(embed = pages[i])
                    await updateReactions(statsMsg)
            elif str(reaction) == '▶':
                if i < 2:
                    i += 1
                    await statsMsg.edit(embed = pages[i])
                    await updateReactions(statsMsg)
            elif str(reaction) == '⏭':
                i = 2
                await statsMsg.edit(embed = pages[i])
                await updateReactions(statsMsg)
            elif str(reaction) == '❌':
                break;
                
            try:
                reaction, user = await self.wait_for('reaction_add', timeout = 30.0, check = check)
            except:
                break

        await statsMsg.clear_reactions()
            

    async def synergy(self, ctx, components):
        await ctx.reply('synergy', mention_author=True)

    async def handleCommand(self, ctx, components):
        print(components)

        if components == []:
            await self.help(ctx)
        
        command = components[0].lower();

        if command == 'ladder':
            await self.ladder(ctx)
        elif command == 'stats':
            await self.stats(ctx, components[1:])
        elif command == 'synergy':
            await self.synergy(ctx)
        elif command == 'statsview' or command == 'stats_view':
            await ctx.reply(STATS_VIEW, mention_author=True)
        elif command == 'statslink' or command == 'stats_link':
            await ctx.reply(STATS_LINK, mention_author=True)
        elif command == 'help':
            await self.help(ctx)
        else:
            await self.help(ctx)




    

client = MyClient()
client.run(SchneckyIRLBotToken)




