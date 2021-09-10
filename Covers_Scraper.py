import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv

class game:
    def __init__(self, home, away, date, time):
        self.home = home
        self.away = away
        self.date = date
        self.time = time
        odds_list = []
    def set_odds(self, book_name, home_odds, away_odds):
        odds_list.append(odds(book_name, home_odds, away_odds))
    def __str__(self):
        return (f' {self.away} @ {self.home} - {self.date}  {self.time} {odds_list}')

class odds:
    def __init__(self, book_name, home_odds, away_odds):
        self.book_name = book_name
        self.home_odds = home_odds
        self.away_odds = away_odds


if __name__=="__main__": 
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    url = "https://www.covers.com/football/ncaaf/odds"
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")

#gets week's schedule
    game_list = []
    table_covers = soup.find('table', class_="table __OpenOddsTable covers-CoversMatchups-Table covers-CoversOdds-gamelineTable covers-CoversComponents-fixedColumn")
    table_covers_rows = table_covers.find_all('tr', class_="covers-CoversComponents-fixedColumnRow")
    for r in table_covers_rows:
        date = ((r.find('div', class_="__date").text).rstrip(" \n").lstrip(" \n\r"))
        time = ((r.find('div', class_="__time").text).rstrip(" \n").lstrip(" \n\r"))
        teams = r.find_all('span', class_="__fullname")
        away = teams[0].text
        home = teams[1].text
        game_list.append(game(home, away, date, time))

    for g in game_list:
        #get odds from each book, create odds object and add to list of odds in each game object
        
        g.set_odds(book_name, home_odds, away_odds)

#gets each game's odds
    odds_list = []
    table_odds = soup.find('table', class_="table __OddsTable covers-CoversMatchups-Table covers-CoversOdds-gamelineTable covers-CoversOdds-odssTableSpecial covers-CoversComponents-fixedHeaderTable")
    table_odds_rows = table_odds.find_all('tr', class_="covers-CoversOdds-mainTR")
    for r in table_odds_rows:
        book_list = r.find_all('td', "covers-CoversMatchups-centerAlignHelper covers-CoversOdss-oddsTd covers-CoversOdds-odssTdSpecial liveOddsCell")
        odds_list = book_list.find_all('div', class_="__bookOdds") #this line causing error, resultset does not have find_all
        for p in odds_list:
            book = p.find_all('span', class_="__decimal")
            home_odds = book.s1.text
            away_odds = book.s2.text


#Read/write operations, should at some point incorporate datetime and write a new file for each week
    filename = "D:\Programming\Arb_Calc\Arb_Results.csv"
    with open(filename, 'w') as file:
        writer = csv.writer(file, lineterminator = '\n') 
        fields = ['Home', 'Away', 'Date', 'Time']
        writer.writerow(fields)
        for g in game_list:
            fields = [g.home, g.away, g.date, g.time]
            writer.writerow(fields)
