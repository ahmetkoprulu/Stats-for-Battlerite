from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import requests, json, operator

import pybattlerite

class Champion:
    def __init__(self, name, lv, xp, totWin, totLoss, playTime, rank2v2Win, rank2v2Loss, rank3v3Win, rank3v3Loss, unrank2v2Win,
                 unrank2v2Loss, unrank3v3Win, unrank3v3Loss):
        self.name = name
        self.lv = lv # 40001
        self.xp = xp
        self.totWin = totWin
        self.totLoss = totLoss

        self.totMatch = totWin + totLoss

        if self.totWin == 0:
            self.winrate = 0
        else:
            self.winrate = self.totWin / (self.totWin + self.totLoss) * 100

        self.txtwinrate = str(self.winrate)[:4]

        self.playTime = playTime

        self.rank2v2Win = rank2v2Win
        self.rank2v2Loss = rank2v2Loss
        self.rank3v3Win = rank3v3Win
        self.rank3v3Loss = rank3v3Loss
        self.unrank2v2Win = unrank2v2Win
        self.unrank2v2Loss = unrank2v2Loss
        self.unrank3v3Win = unrank3v3Win
        self.unrank3v3Loss = unrank3v3Loss


class Player:
    def __init__(self, id, name, title, pic, accLvl, totchamplv,
                 wins, losses, timePlayed, Unranked2v2Losses, Unranked2v2Wins, Unranked3v3Wins, Unranked3v3Losses, Ranked2v2Wins, Ranked2v2Losses, Ranked3v3Losses, Ranked3v3Wins, BrawlWins, BrawlLosses,
                 ):

        # Header Info-------------------------------------------------------
        self.id = id
        self.name = name
        self.title = title
        self.pic = pic
        self.accLvl = accLvl # 26
        self.totchamplv = totchamplv
        # Match Wins/Losses--------------------------------------------------
        self.wins = wins # 2
        self.losses = losses # 3
        self.timePlayed = timePlayed # 8
        self.Unranked2v2Wins = Unranked2v2Wins #10
        self.Unranked2v2Losses = Unranked2v2Losses #11
        self.Unranked3v3Wins = Unranked3v3Wins # 12
        self.Unranked3v3Losses = Unranked3v3Losses # 13
        self.Ranked2v2Wins = Ranked2v2Wins #14
        self.Ranked2v2Losses = Ranked2v2Losses # 15
        self.Ranked3v3Wins = Ranked3v3Wins # 16
        self.Ranked3v3Losses = Ranked3v3Losses # 17
        self.BrawlWins = BrawlWins #18
        self.BrawlLosses = BrawlLosses #19

        # Win Rates----------------------------------------------------------------
        if self.wins == 0:
            self.winrate = 0
        else:
            self.winrate = wins/(wins + losses) * 100
        self.txtwinrate = str(self.winrate)[:4]

        if self.Ranked2v2Wins == 0:
            self.rank2v2Winrate = 0
        else:
            self.rank2v2Winrate = Ranked2v2Wins/(Ranked2v2Wins + Ranked2v2Losses) * 100
        self.txtrank2v2winrate = str(self.rank2v2Winrate)[:4]

        if self.Ranked3v3Wins == 0:
            self.rank3v3winrate = 0
        else:
            self.rank3v3winrate = Ranked3v3Wins/(Ranked3v3Wins + Ranked3v3Losses) * 100
        self.txtrank3v3winrate = str(self.rank3v3winrate)[:4]

        if self.Unranked2v2Wins == 0:
            self.unrank2v2winrate = 0
        else:
            self.unrank2v2winrate = Unranked2v2Wins/(Unranked2v2Wins + Unranked2v2Losses) * 100
        self.txtunrank2v2winrate = str(self.unrank2v2winrate)[:4]

        if self.Unranked3v3Wins == 0:
            self.unrank3v3winrate = 0
        else:
            self.unrank3v3winrate = Unranked3v3Wins/(Unranked3v3Wins + Unranked3v3Losses) * 100
        self.txtunrak3v3winrate = str(self.unrank3v3winrate)[:4]


class Streamer:
    def __init__(self, id, name, logo, status, partner, url, viewer, preview_md, lang):
        self.id = id
        self.name = name
        self.logo = logo
        self.status = status
        self.partner = partner
        self.url = url
        self.viewer = viewer
        self.preview_md = preview_md
        self.lang = lang
# class Team:
#     def __init__(self, soloteam, solodivision, soloname, team2v2league, team2v2division, team2v2name, team2v2pic, team2v2rankname, team3v3league, team3v3division, team3v3name, team3v3pic, team3v3rankname):
#         self.soloteam = soloteam
#         self.solodivision = solodivision
#         self.solopic = soloname
#         self.team2v2league = team2v2league
#         self.team2v2division = team2v2division
#         self.team2v2name = team2v2name
#         self.team2v2pic = team2v2pic
#         self.team2v2rankname = team2v2rankname
#         self.team3v3league = team3v3league
#         self.team3v3division = team3v3division
#         self.team3v3name = team3v3name
#         self.team3v3pic = team3v3pic
#         self.team3v3rankname = team3v3rankname


brc = pybattlerite.Client(
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZTg0YzdhMC1iNjkwLTAxMzUtNmFiMS0wYTU4NjQ2MGRiMzAiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTExODkwNDY3LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoidG9vbHMtZm9yLWJhdHRsZXJpdGUiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.UbiFOD_RZ3qyN4PiFrlC5uwzoW_Ak9aJsKQZZVtO12I')

app = Flask(__name__)



BASE_URL_TW = 'https://api.twitch.tv/kraken/streams/'

header_tw = {
    "Client-ID": "kyghnve1civy7doxv3o056szwj0bs7",
    "Accept": "application/vnd.twitchtv.v5+json"
}

pic_dic = {"39001": "Drop_01", "39002": "Drop_02", "39003": "Drop_03", "39004": "Drop_04", "39005": "Drop_05",
           "39006": "Drop_06", "39007": "Drop_07", "39008": "Drop_08", "39009": "Drop_09", "39010": "Drop_10",
           "39011": "Drop_11", "39012": "Drop_12", "39013": "Drop_13", "39014": "Drop_14", "39015": "Drop_15",
           "39016": "Drop_16", "39017": "Drop_17", "39018": "Drop_18", "39019": "Drop_19", "39020": "Drop_20",
           "39021": "Drop_21", "39022": "Drop_22", "39023": "Drop_23", "39024": "Drop_24", "39025": "Drop_25",
           "39026": "Drop_26", "39027": "Drop_27", "39028": "Drop_28", "39029": "Drop_29", "39030": "Drop_30",
           "39031": "Drop_31", "39032": "Drop_32", "39033": "Drop_33", "39034": "Drop_34", "39035": "Drop_35",
           "39036": "Drop_36", "39037": "Drop_37", "39038": "Drop_38", "39039": "Drop_39", "39040": "Drop_40",
           "39041": "Drop_41", "39042": "Drop_42", "39043": "Drop_43", "39044": "Drop_44", "39045": "Drop_45",
           "39046": "Drop_46", "39047": "Drop_47", "39048": "Drop_48", "39049": "Drop_49", "39050": "Drop_50",
           "39051": "Drop_51", "39052": "Drop_52", "39053": "Drop_53", "39054": "Drop_54", "39055": "Drop_55",
           "39056": "Drop_56", "39057": "Drop_57", "39058": "Drop_58", "39059": "Drop_59", "39060": "Drop_60",
           "39061": "Drop_61", "39062": "Drop_62", "39063": "Drop_63", "39064": "Drop_64", "39065": "Drop_65",
           "39066": "Drop_66", "39067": "Drop_67", "39068": "Drop_68", "39069": "Drop_69", "39070": "Drop_70",
           "39071": "Drop_71", "39072": "Drop_72", "39073": "Drop_73", "39074": "Drop_74", "39075": "Drop_75",
           "39076": "Drop_76", "30001": "Progression_Lucie", "30002": "Progression_Sirius", "30003": "Progression_Iva",
           "30004": "Progression_Jade", "30005": "Progression_Harbinger", "30006": "Progression_Oldur", "30007": "Progression_Ashka",
           "30008": "Progression_Varesh", "30009": "Progression_Pearl", "300010": "Progression_Taya", "30011": "Progression_Poloma",
           "30012": "Progression_Croak", "30013": "Progression_Freya", "30014": "Progression_Jumong", "30015": "Progression_Shifu",
           "30016": "Progression_Ezmo", "30017": "Progression_Bakko", "30018": "Progression_Rook", "30019": "Progression_Pestilus",
           "30020": "Progression_Destiny", "30021": "Progression_Swordguy", "30022": "Progression_Blossom", "30025": "Progression_Thorn",
           "30035": "Progression_Zander", "30041": "Progression_Alysia", "34001": "qa",
           "30000": "DefaultAvatar", "39500": "StarterAvatar", "39501": "AlphaAvatar", "39505": "BetaAvatar",
           "34501": "SteamAshkaTrain", "34502": "NewYear2017", "34503": "Christmas2017", "39503": "StreamerAvatar", "39504": "SupporterAvatar", "39506": "FounderAvatar",
           "36000": "Season01_Bronze", "36001": "Season01_Silver", "36002": "Season01_Gold", "36003": "Season01_Platinum", "36004": "Season01_Diamond", "36005": "Season01_Champion", "36006": "Season01_GrandChampion",
           "36007": "Season02_Bronze", "36008": "Season02_Silver", "36009": "Season02_Gold", "36010": "Season02_Platinum", "36011": "Season02_Diamond", "36012": "Season02_Champion", "36013": "Season02_GrandChampion",
           "36014": "Season03_Bronze", "36015": "Season03_Silver", "36016": "Season03_Gold", "36017": "Season03_Platinum", "36018": "Season03_Diamond", "36019": "Season03_Champion", "36020": "Season03_GrandChampion",
           "36021": "Season04_Bronze", "36022": "Season04_Silver", "36023": "Season04_Gold", "36024": "Season04_Platinum", "36025": "Season04_Diamond", "36026": "Season04_Champion", "36027": "Season04_GrandChampion",
           "36028": "Season05_Bronze", "36029": "Season05_Silver", "36030": "Season05_Gold", "36031": "Season05_Platinum", "36032": "Season05_Diamond", "36033": "Season05_Champion", "36034": "Season05_GrandChampion",
           "36035": "PreSeason_Bronze", "36036": "PreSeason_Silver", "36037": "PreSeason_Gold", "36038": "PreSeason_Platinum", "36039": "PreSeason_Diamond", "36040": "PreSeason_Champion", "36041": "PreSeason_GrandChampion",
           "38001": "Hafu_Custom", "38002": "StunlockAvatar", "38003": "MastersOfBaconAvatar_01", "38004": "Tournament_Winner_01", "39201": "Halloween_01", "39202": "Halloween_02", "39203": "Halloween_03", "39204": "Halloween_04",
           "39205": "Halloween_05", "39206": "Halloween_06", "39207": "Halloween_07", "39208": "Halloween_08", "39209": "Halloween_09", "39210": "Halloween_10", "39211": "Christmas_01", "39212": "Christmas_02", "39213": "Christmas_03",
           "39214": "Christmas_04", "39215": "Christmas_05", "39216": "Christmas_06", "39217": "Christmas_07", "39218": "Christmas_08", "39219": "Christmas_09", "39220": "Christmas_10",
           "39221": "Valentines_01", "39222": "Valentines_02", "39223": "Valentines_03", "39224": "prehistoric_00", "39225": "prehistoric_01", "39226": "prehistoric_02", "39227": "prehistoric_03", "39228": "prehistoric_04", "39229": "prehistoric_05",
           "39230": "prehistoric_06", "39231": "prehistoric_07", "39232": "prehistoric_08", "39233": "prehistoric_09", "39234": "prehistoric_10", "39235": "prehistoric_11", "39236": "prehistoric_12", "39237": "prehistoric_13", "39238": "prehistoric_14",
           "39239": "prehistoric_15", "39240": "prehistoric_16", "39241": "prehistoric_17", "39242": "prehistoric_18", "39243": "prehistoric_19", "39244": "Christmas_11", "39245": "Christmas_12", "39246": "Christmas_13", "39247": "Christmas_14", "39248": "Christmas_15",
           "39249": "Christmas_16", "39250": "Christmas_17", "39251": "Christmas_18", "39252": "Christmas_19", "39253": "Christmas_20", "39254": "Lunar_01", "39255": "Lunar_02", "39256": "Lunar_03", "39257": "Lunar_04", "39258": "Lunar_05", "39259": "Lunar_06",
           "39260": "Lunar_07", "39261": "Lunar_08", "39262": "Lunar_09", "39263": "Lunar_10", "39264": "Lunar_11", "39265": "Lunar_12", "39266": "Lunar_13", "39267": "Lunar_14", "39268": "Lunar_15", "39269": "Lunar_16", "39270": "Lunar_17", "39271": "Lunar_18", "39272": "Lunar_19", "39273": "Lunar_20",
           "39508": "Season01", "39509": "TwitchCommerce_01", "39510": "RivalEsportsAvatar", "0": "DefaultAvatar"}

tit = {500: "alpha tester", 501: "Developer", 502: "Beta Tester", 503: "founder", 504: "contender",
       505: "The Filmmaker", 506: "Spirit Catcher", 507: "Battle Rekt Salt Miner", 508: "ESL Monthly Champion",
       509: "ESL Monthly Elite", 510: "Enter The Arena Champion", 511: "King Of The Arena 2v2", 512: "King Of The Arena 3v3",
       513: "Art Warrior", 31001: "Expelled Alchemist", 31002: "The Zenith",
       31003: "The Scavenging Inventor", 31004: "Lone Gunner", 31005: "Crypt Warden", 31006: "The Time Mender",
       31007: "The Molten Fury", 31008: "The Eternal", 31009: "The Ocean Sage", 31010: "The Wind Of The West",
       31011: "The Psychopomp", 31012: "The Ranid Assassin", 31013: "The Eye Of The Storm", 31014: "The Beast Hunter",
       31015: "The Spear", 31016: "The Mischievous", 31017: "Hero Of Boulder Pass", 31018: "The Hungering Berserker",
       31019: "Lord Of Swarm", 31020: "The Exiled Prince", 31021: "The Forest Mender",
       60000: "#1 S1 Grand Champion Solo", 60001: "#2 S1 Grand Champion Solo", 60002: "#3 S1 Grand Champion Solo",
       60003: "#4 S1 Grand Champion Solo", 60004: "#5 S1 Grand Champion", 60005: "#1 S1 Grand Champion 2v2",
       60006: "#2 S1 Grand Champion 2v2", 60007: "#3 S1 Grand Champion 2v2", 60008: "#4 S1 Grand Champion 2v2",
       60009: "#5 S1 Grand Champion 2v2", 60010: "#1 S1 Grand Champion 3v3", 60011: "#2 S1 Grand Champion 3v3",
       60012: "#3 S1 Grand Champion 3v3", 60013: "#4 S1 Grand Champion 3v3", 60014: "#5 S1 Grand Champion 3v3",
       60015: "#1 S2 Grand Champion Solo", 60016: "#2 S2 Grand Champion Solo", 60017: "#3 S2 Grand Champion Solo",
       60018: "#4 S2 Grand Champion Solo", 60019: "#5 S2 Grand Champion Solo", 60020: "#1 S2 Grand Champion 2v2",
       60021: "#2 S2 Grand Champion 2v2", 60022: "#3 S2 Grand Champion 2v2", 60023: "#4 S2 Grand Champion 2v2",
       60024: "#5 S2 Grand Champion 2v2", 60025: "#1 S2 Grand Champion 3v3", 60026: "#2 S2 Grand Champion 3v3",
       60027: "#3 S2 Grand Champion 3v3", 60028: "#4 S2 Grand Champion 3v3", 60029: "#5 S2 Grand Champion 3v3",
       60030: "#1 S3 Grand Champion Solo", 60031: "#2 S3 Grand Champion Solo", 60032: "#3 S3 Grand Champion Solo",
       60033: "#4 S3 Grand Champion Solo", 60034: "#5 S3 Grand Champion Solo", 60035: "#1 S3 Grand Champion 2v2",
       60036: "#2 S3 Grand Champion 2v2", 60037: "#3 S4 Grand Champion 2v2", 60038: "#4 S3 Grand Champion 2v2",
       60039: "#5 S3 Grand Champion 2v2", 60040: "#1 S3 Grand Champion 3v3", 60041: "#2 S3 Grand Champion 3v3",
       60042: "#3 S3 Grand Champion 3v3", 60043: "#4 S3 Grand Champion 3v3", 60044: "#5 S3 Grand Champion 3v3",
       60045: "#1 S4 Grand Champion Solo", 60046: "#2 S4 Grand Champion Solo",
       60047: "#3 S4 Grand Champion Solo", 60048: "#4 S4 Grand Champion Solo", 60049: "#5 S4 Grand Champion Solo",
       60050: "#1 S4 Grand Champion 2v2", 60051: "#2 S4 Grand Champion 2v2",
       60052: "#3 S4 Grand Champion 2v2", 60053: "#4 S4 Grand Champion 2v2", 60054: "#5 S4 Grand Champion 2v2",
       60055: "#1 S4 Grand Champion 3v3", 60056: "#2 S4 Grand Champion 3v3",
       60057: "#3 S4 Grand Champion 3v3", 60058: "#4 S4 Grand Champion 3v3", 60059: "#5 S4 Grand Champion 3v3",
       60060: "#1 S5 Grand Champion Solo", 60061: "#2 S5 Grand Champion Solo",
       60062: "#3 S5 Grand Champion Solo", 60063: "#4 S5 Grand Champion Solo", 60064: "#5 S5 Grand Champion Solo",
       60065: "#1 S5 Grand Champion 2v2", 60066: "#2 S5 Grand Champion 2v2",
       60067: "#3 S5 Grand Champion 2v2", 60068: "#4 S5 Grand Champion 2v2", 60069: "#5 S5 Grand Champion 2v2",
       60070: "#1 S5 Grand Champion 3v3", 60071: "#2 S5 Grand Champion 3v3",
       60072: "#3 S5 Grand Champion 3v3", 60073: "#4 S5 Grand Champion 3v3", 60074: "#5 S5 Grand Champion 3v3",
       60075: "#1 S6 Grand Champion Solo", 60076: "#2 S6 Grand Champion Solo",
       60077: "#3 S6 Grand Champion Solo", 60078: "#4 S6 Grand Champion Solo", 60079: "#5 S5 Grand Champion Solo",
       60080: "#1 S6 Grand Champion 2v2", 60081: "#2 S6 Grand Champion 2v2",
       60082: "#3 S6 Grand Champion 2v2", 60083: "#4 S6 Grand Champion 2v2", 60084: "#5 S5 Grand Champion 2v2",
       60085: "#1 S6 Grand Champion 3v3", 60086: "#2 S6 Grand Champion 3v3",
       60087: "#3 S6 Grand Champion 3v3", 60088: "#4 S6 Grand Champion 3v3", 60089: "#5 S5 Grand Champion 3v3",
       60090: "Message Deleted"
       }

league_dic = {None: "Placements", "0": "Bronze League", "1": "Silver League", "2": "Gold League",
              "3": "Platinum League", "4": "Diamond League", "5": "Champion League", "6": "Grand Champion"}

champNameDic = {
    467463015: "Lucie", 259914044: "Sirius", 842211418: "Iva", 65687534: "Jade", 1649551456: "Pestulus",  543520739: "Blossom",
    613085868: "Alysia", 1318732017: "Rook", 550061327: "Ruh Kaan", 1908945514: "Oldur", 369797039: "Varesh", 44962063: "Pearl",
    870711570: "Destiny", 154382530: "Taya", 1134478706: "Poloma", 1208445212: "Croak", 1606711539: "Freya", 39373466: "Jumong",
    763360732: "Shifu", 1377055301: "Ezmo", 1749055646: "Raigon", 1463164578: "Thorn", 1422481252: "Bakko", 1496688063: "Zander",
    1: "Ashka"
}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    username = request.form['username']
    return redirect(url_for('view_profile', player_name=username))


@app.route('/profile/<player_name>')
def view_profile(player_name):

    # request for Player info -------------------------------------------------------------------------------------------
    query = {
        'filter[playerNames]': player_name
    }

    r = requests.get(BASE_URL + "/players", headers=header, params=query)
    data = json.loads(r.text)

    print(data['data'][0]['attributes'])

    p_stats = data['data'][0]['attributes']['stats']

    id = data['data'][0]['id']
    name = data['data'][0]['attributes']['name']
    picture_link = "Avatar_" + pic_dic[str(p_stats['picture'])] + ".png"
    title = tit[p_stats['title']]

    champ_dic = {

        'Lucie': Champion('Lucie', p_stats.get('40001', 0), p_stats.get('11001', 0), p_stats.get('12001', 0),
                          p_stats.get('13001', 0), p_stats.get('16001', 0), p_stats.get('17001', 0),
                          p_stats.get('18001', 0), p_stats.get('19001', 0), p_stats.get('20001', 0),
                          p_stats.get('21001', 0), p_stats.get('22001', 0), p_stats.get('23001', 0),
                          p_stats.get('24001', 0)),

        'Sirius': Champion('Sirius', p_stats.get('40002', 0), p_stats.get('11002', 0), p_stats.get('12002', 0),
                           p_stats.get('13002', 0), p_stats.get('16002', 0), p_stats.get('17002', 0),
                           p_stats.get('18002', 0), p_stats.get('19002', 0), p_stats.get('20002', 0),
                           p_stats.get('21002', 0), p_stats.get('22002', 0), p_stats.get('23002', 0),
                           p_stats.get('24002', 0)),

        'Iva': Champion('Iva', p_stats.get('40003', 0), p_stats.get('11003', 0), p_stats.get('12003', 0),
                        p_stats.get('13003', 0), p_stats.get('16003', 0), p_stats.get('17003', 0),
                        p_stats.get('18003', 0), p_stats.get('19003', 0), p_stats.get('20003', 0),
                        p_stats.get('21003', 0), p_stats.get('22003', 0), p_stats.get('23003', 0),
                        p_stats.get('24003', 0)),

        'Jade': Champion('Jade', p_stats.get('40004', 0), p_stats.get('11004', 0), p_stats.get('12004', 0),
                         p_stats.get('13004', 0), p_stats.get('16004', 0), p_stats.get('17004', 0),
                         p_stats.get('18004', 0), p_stats.get('19004', 0), p_stats.get('20004', 0),
                         p_stats.get('21004', 0), p_stats.get('22004', 0), p_stats.get('23004', 0),
                         p_stats.get('24004', 0)),

        'Ruh Kaan': Champion('Ruh Kaan', p_stats.get('40005', 0), p_stats.get('11005', 0), p_stats.get('12005', 0),
                             p_stats.get('13005', 0), p_stats.get('16005', 0), p_stats.get('17005', 0),
                             p_stats.get('18005', 0), p_stats.get('19005', 0), p_stats.get('20005', 0),
                             p_stats.get('21005', 0), p_stats.get('22005', 0), p_stats.get('23005', 0),
                             p_stats.get('24005', 0)),

        'Oldur': Champion('Oldur', p_stats.get('40006', 0), p_stats.get('11006', 0), p_stats.get('12006', 0),
                          p_stats.get('13006', 0), p_stats.get('16006', 0), p_stats.get('17006', 0),
                          p_stats.get('18006', 0), p_stats.get('19006', 0), p_stats.get('20006', 0),
                          p_stats.get('21006', 0), p_stats.get('22006', 0), p_stats.get('23006', 0),
                          p_stats.get('24006', 0)),

        'Ashka': Champion('Ashka', p_stats.get('40007', 0), p_stats.get('11007', 0), p_stats.get('12007', 0),
                          p_stats.get('13007', 0), p_stats.get('16007', 0), p_stats.get('17007', 0),
                          p_stats.get('18007', 0), p_stats.get('19007', 0), p_stats.get('20007', 0),
                          p_stats.get('21007', 0), p_stats.get('22007', 0), p_stats.get('23007', 0),
                          p_stats.get('24007', 0)),

        'Varesh': Champion('Varesh', p_stats.get('40008', 0), p_stats.get('11008', 0), p_stats.get('12008', 0),
                           p_stats.get('13008', 0), p_stats.get('16008', 0), p_stats.get('17008', 0),
                           p_stats.get('18008', 0), p_stats.get('19008', 0), p_stats.get('20008', 0),
                           p_stats.get('21008', 0), p_stats.get('22008', 0), p_stats.get('23008', 0),
                           p_stats.get('24008', 0)),

        'Pearl': Champion('Pearl', p_stats.get('40009', 0), p_stats.get('11009', 0), p_stats.get('12009', 0),
                          p_stats.get('13009', 0), p_stats.get('16009', 0), p_stats.get('17009', 0),
                          p_stats.get('18009', 0), p_stats.get('19009', 0), p_stats.get('20009', 0),
                          p_stats.get('21009', 0), p_stats.get('22009', 0), p_stats.get('23009', 0),
                          p_stats.get('24009', 0)),

        'Taya': Champion('Taya', p_stats.get('40010', 0), p_stats.get('11010', 0), p_stats.get('12010', 0),
                         p_stats.get('13010', 0), p_stats.get('16010', 0), p_stats.get('17010', 0),
                         p_stats.get('18010', 0), p_stats.get('19010', 0), p_stats.get('20010', 0),
                         p_stats.get('21010', 0), p_stats.get('22010', 0), p_stats.get('23010', 0),
                         p_stats.get('24010', 0)),

        'Poloma': Champion('Poloma', p_stats.get('40011', 0), p_stats.get('11011', 0), p_stats.get('12011', 0),
                           p_stats.get('13011', 0), p_stats.get('16011', 0), p_stats.get('17011', 0),
                           p_stats.get('18011', 0), p_stats.get('19011', 0), p_stats.get('20011', 0),
                           p_stats.get('21011', 0), p_stats.get('22011', 0), p_stats.get('23011', 0),
                           p_stats.get('24011', 0)),

        'Croak': Champion('Croak', p_stats.get('40012', 0), p_stats.get('11012', 0), p_stats.get('12012', 0),
                          p_stats.get('13012', 0), p_stats.get('16012', 0), p_stats.get('17012', 0),
                          p_stats.get('18012', 0), p_stats.get('19012', 0), p_stats.get('20012', 0),
                          p_stats.get('21012', 0), p_stats.get('22012', 0), p_stats.get('23012', 0),
                          p_stats.get('24012', 0)),

        'Freya': Champion('Freya', p_stats.get('40013', 0), p_stats.get('11013', 0), p_stats.get('12013', 0),
                          p_stats.get('13013', 0), p_stats.get('16013', 0), p_stats.get('17013', 0),
                          p_stats.get('18013', 0), p_stats.get('19013', 0), p_stats.get('20013', 0),
                          p_stats.get('21013', 0), p_stats.get('22013', 0), p_stats.get('23013', 0),
                          p_stats.get('24013', 0)),

        'Jumong': Champion('Jumong', p_stats.get('40014', 0), p_stats.get('11014', 0), p_stats.get('12014', 0),
                           p_stats.get('13014', 0), p_stats.get('16014', 0), p_stats.get('17014', 0),
                           p_stats.get('18014', 0), p_stats.get('19014', 0), p_stats.get('20014', 0),
                           p_stats.get('21014', 0), p_stats.get('22014', 0), p_stats.get('23014', 0),
                           p_stats.get('24014', 0)),

        'Shifu': Champion('Shifu', p_stats.get('40015', 0), p_stats.get('11015', 0), p_stats.get('12015', 0),
                          p_stats.get('13015', 0), p_stats.get('16015', 0), p_stats.get('17015', 0),
                          p_stats.get('18015', 0), p_stats.get('19015', 0), p_stats.get('20015', 0),
                          p_stats.get('21015', 0), p_stats.get('22015', 0), p_stats.get('23015', 0),
                          p_stats.get('24015', 0)),

        'Ezmo': Champion('Ezmo', p_stats.get('40016', 0), p_stats.get('11016', 0), p_stats.get('12016', 0),
                         p_stats.get('13016', 0), p_stats.get('16016', 0), p_stats.get('17016', 0),
                         p_stats.get('18016', 0), p_stats.get('19016', 0), p_stats.get('20016', 0),
                         p_stats.get('21016', 0), p_stats.get('22016', 0), p_stats.get('23016', 0),
                         p_stats.get('24016', 0)),

        'Bakko': Champion('Bakko', p_stats.get('40017', 0), p_stats.get('11017', 0), p_stats.get('12017', 0),
                          p_stats.get('13017', 0), p_stats.get('16017', 0), p_stats.get('17017', 0),
                          p_stats.get('18017', 0), p_stats.get('19017', 0), p_stats.get('20017', 0),
                          p_stats.get('21017', 0), p_stats.get('22017', 0), p_stats.get('23017', 0),
                          p_stats.get('24017', 0)),

        'Rook': Champion('Rook', p_stats.get('40018', 0), p_stats.get('11018', 0), p_stats.get('12018', 0),
                         p_stats.get('13018', 0), p_stats.get('16018', 0), p_stats.get('17018', 0),
                         p_stats.get('18018', 0), p_stats.get('19018', 0), p_stats.get('20018', 0),
                         p_stats.get('21018', 0), p_stats.get('22018', 0), p_stats.get('23018', 0),
                         p_stats.get('24018', 0)),

        'Pestilus': Champion('Pestilus', p_stats.get('40019', 0), p_stats.get('11019', 0), p_stats.get('12019', 0),
                             p_stats.get('13019', 0), p_stats.get('16019', 0), p_stats.get('17019', 0),
                             p_stats.get('18019', 0), p_stats.get('19019', 0), p_stats.get('20019', 0),
                             p_stats.get('21019', 0), p_stats.get('22019', 0), p_stats.get('23019', 0),
                             p_stats.get('24019', 0)),

        'Destiny': Champion('Destiny', p_stats.get('40020', 0), p_stats.get('11020', 0), p_stats.get('12020', 0),
                            p_stats.get('13020', 0), p_stats.get('16020', 0), p_stats.get('17020', 0),
                            p_stats.get('18020', 0), p_stats.get('19020', 0), p_stats.get('20020', 0),
                            p_stats.get('21020', 0), p_stats.get('22020', 0), p_stats.get('23020', 0),
                            p_stats.get('24020', 0)),

        'Raigon': Champion('Raigon', p_stats.get('40021', 0), p_stats.get('11021', 0), p_stats.get('12021', 0),
                           p_stats.get('13021', 0), p_stats.get('16021', 0), p_stats.get('17021', 0),
                           p_stats.get('18021', 0), p_stats.get('19021', 0), p_stats.get('20021', 0),
                           p_stats.get('21021', 0), p_stats.get('22021', 0), p_stats.get('23021', 0),
                           p_stats.get('24021', 0)),

        'Blossom': Champion('Blossom', p_stats.get('40022', 0), p_stats.get('11022', 0), p_stats.get('12022', 0),
                            p_stats.get('13022', 0), p_stats.get('16022', 0), p_stats.get('17022', 0),
                            p_stats.get('18022', 0), p_stats.get('19022', 0), p_stats.get('20022', 0),
                            p_stats.get('21022', 0), p_stats.get('22022', 0), p_stats.get('23022', 0),
                            p_stats.get('24022', 0)),

        'Thorn': Champion('Thorn', p_stats.get('40025', 0), p_stats.get('11025', 0), p_stats.get('12025', 0),
                          p_stats.get('13025', 0), p_stats.get('16025', 0), p_stats.get('17025', 0),
                          p_stats.get('18025', 0), p_stats.get('19025', 0), p_stats.get('20025', 0),
                          p_stats.get('21025', 0), p_stats.get('22025', 0), p_stats.get('23025', 0),
                          p_stats.get('24025', 0)),

        'Zander': Champion('Zander', p_stats.get('40035', 0), p_stats.get('11035', 0), p_stats.get('12035', 0),
                           p_stats.get('13035', 0), p_stats.get('16035', 0), p_stats.get('17035', 0),
                           p_stats.get('18035', 0), p_stats.get('19035', 0), p_stats.get('20035', 0),
                           p_stats.get('21035', 0), p_stats.get('22035', 0), p_stats.get('23035', 0),
                           p_stats.get('24035', 0)),

        'Alysia': Champion('Alysia', p_stats.get('40041', 0), p_stats.get('11041', 0), p_stats.get('12041', 0),
                           p_stats.get('13041', 0), p_stats.get('16041', 0), p_stats.get('17041', 0),
                           p_stats.get('18041', 0), p_stats.get('19041', 0), p_stats.get('20041', 0),
                           p_stats.get('21041', 0), p_stats.get('22041', 0), p_stats.get('23041', 0),
                           p_stats.get('24041', 0)),

    }

    # Sorting champions by macth played---------------------------------------------------------------------------------
    champ_sorted = []
    champ_sorted2 = []
    totchamplv = 0

    for champ in reversed(sorted(champ_dic.values(), key=operator.attrgetter('totMatch'))):
        print(str(champ.winrate))
        if len(champ_sorted) > 2:
            champ_sorted2.append(champ)
            totchamplv += champ.lv
        else:
            totchamplv += champ.lv
            champ_sorted.append(champ)
            champ_sorted2.append(champ)

    player = Player(id, name, title, picture_link, p_stats.get('26', 0), totchamplv, p_stats.get('2', 0),
                    p_stats.get('3', 0), p_stats.get('8', 0), p_stats.get('10', 0), p_stats.get('11', 0),
                    p_stats.get('12', 0), p_stats.get('13', 0), p_stats.get('14', 0), p_stats.get('15', 0),
                    p_stats.get('16', 0), p_stats.get('17', 0), p_stats.get('18', 0), p_stats.get('19', 0), )

# Parsing Ranked Teams--------------------------------------------------------------------------------------------------
    teams = brc.get_teams(playerids=[player.id], season=6)
    teams2v2 = []
    teams3v3 = []
    solorank = 0

    print(teams)
# Seperating teams by solo, 2v2, 3v3------------------------------------------------------------------------------------
    for i in teams:
        if len(i.members) == 2:
            teams2v2.append(i)
        elif len(i.members) == 3:
            teams3v3.append(i)
        else:
            solorank = i

    teams2v2.sort(key=lambda x: x.league, reverse=True)
    teams3v3.sort(key=lambda x: x.league, reverse=True)

    participants = []
    for j in teams2v2[0].members:
        if j not in participants:
            participants.append(j)

    for i in teams3v3[0].members:
        if i not in participants:
            participants.append(i)

    print(str(participants)+"\n")
    print(len(participants))

    players = brc.get_players(playerids=participants)

    print(players)

    par_ar = []
    for i in players:
        par_ar.append([i.id, i.name, 'Avatar_' + pic_dic[str(i.picture)]])

    print(par_ar)

    temp_mem = []
    for i in teams3v3[0].members:
        for j in par_ar:
            if i == j[0]:
                temp_mem.append(j)

    top3v3 = [teams3v3[0], 'Avatar_'+pic_dic[str(teams3v3[0].avatar)], league_dic[str(teams3v3[0].league)], temp_mem]

    temp_mem = []
    for i in teams2v2[0].members:
        for j in par_ar:
            if i == j[0]:
                temp_mem.append(j)

    top2v2 = [teams2v2[0], 'Avatar_'+pic_dic[str(teams2v2[0].avatar)], league_dic[str(teams2v2[0].league)], temp_mem]

    teams = [
        [solorank, league_dic[str(solorank.league)]],
        top2v2,
        top3v3
    ]


# Match history --------------------------------------------------------------------------------------------------------
    match_history = []
    rosters = []
    bff = {}
    actors = {}
    total_match = 0

    from  datetime import datetime,timedelta

    date = (datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        matches = brc.get_matches(playerids=[id], before=str(date))
        for match in matches.matches:
            total_match += 1
            for roster in match.rosters:
                for participant in roster.participants:
                    if participant.player.id == id:
                        match_history.append(
                            [participant, roster, match.game_mode, match.type, calc_duration(match.duration),
                             match.created_at,
                             champNameDic[int(participant.actor)]])
                        rosters.append(roster)
                        if champNameDic[int(participant.actor)] not in actors:
                            # pick number, pick winrate, win number,
                            if roster.won == True:
                                actors[champNameDic[int(participant.actor)]] = [1, 0,
                                                                                champNameDic[int(participant.actor)], 1,
                                                                                0]
                            else:
                                actors[champNameDic[int(participant.actor)]] = [1, 0,
                                                                                champNameDic[int(participant.actor)], 0,
                                                                                0]
                        else:
                            if roster.won == True:
                                actors[champNameDic[int(participant.actor)]][0] += 1
                                actors[champNameDic[int(participant.actor)]][3] += 1
                            else:
                                actors[champNameDic[int(participant.actor)]][0] += 1
    except KeyError:
        pass



    actors_list = []
    for actor in actors:
        actors[actor][1] = ("%d" %(actors[actor][0] * 100 / total_match))
        actors[actor][4] = ("%d" %(actors[actor][3] * 100 / actors[actor][0]))

        actors_list.append(actors[actor])

    actors_list.sort(key=lambda l:l[0], reverse=True)


    for roster in rosters:
        for participant in roster.participants:
            if participant.player.id not in bff:
                bff[participant.player.id] = [participant, 1, participant.player]
            else:
                bff[participant.player.id][1] += 1



    # Contrubution ----------------------------------------------------------------------------------------------------
    for match in match_history:
        tot_score = 0
        for part in match[1].participants:
            if part.score == None:
                continue
            else:
                tot_score += part.score

        if tot_score == 0:
            match.append(0)
        else:
            match.append(int("%d" % (match[0].score * 100 / tot_score)))

    return render_template('deneme.html', player_name=player.id, player=player, team=teams, participants=par_ar,
                           champ_sorted2=champ_sorted2, champ_dic=champ_dic, champ_sorted=champ_sorted,
                           actors=actors_list, match_history=reversed(match_history))

def calc_duration(time):
    min = time / 60
    sec = time % 60

    return ("%dm " %min) + str(sec) + "s"


from datetime import datetime


@app.template_filter()
def timesince(dt, default="just now"):

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default


@app.route('/streams')
def streams():
    query_tw = {
        'game': 'Battlerite'
    }

    r_tw = requests.get(BASE_URL_TW, headers=header_tw, params=query_tw)
    data_tw = json.loads(r_tw.text)

    streams = data_tw['streams']
    print(json.dumps(streams, indent=3))

    profiles = []

    for stream in streams:
        profiles.append(Streamer(stream['_id'], stream['channel']['display_name'], stream['channel']['logo'],
                                 stream['channel']['status'], stream['channel']['partner'], stream['channel']['url'],
                                 stream['viewers'], stream['preview']['medium'],
                                 stream['channel']['broadcaster_language']))

    return render_template('streams.html', profiles=profiles)


@app.route('/upload/<filename>')
def send_img(filename):
    pic_name = 'Avatar_' + str(filename) + ".png"
    print(pic_name)

    return send_from_directory("static/img/avatar", pic_name)


if __name__ == '__main__':
    app.run()
