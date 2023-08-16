import requests
from bs4 import BeautifulSoup
import csv
import datetime

# date validation
while True:
    try:
        date = input("Enter the match date in format MM/DD/YYYY : ")
        dateObject = datetime.datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
    else:
        break
try:
    page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")
except requests.exceptions.RequestException as e:
    print(f"error: {e}")
else:
    def main(page):
        src = page.content
        soup = BeautifulSoup(src,"lxml")
        matchDetails = []
        championships = soup.find_all("div",{'class':'matchCard'})
        
        def getMatchInfo(championships):
            championshipTilte = championships.contents[1].find("h2").text.strip()
            allMatches = championships.contents[3].find_all("li")
            numberOfMatches = len(allMatches)
            for i in range(numberOfMatches):
                #get team names
                teamA = allMatches[i].find("div",{"class": "teamA"}).text.strip()
                teamB = allMatches[i].find("div",{"class": "teamB"}).text.strip()

                #get score
                matchResult = allMatches[i].find("div",{"class":"MResult"}).find_all("span",{"class":"score"})
                score = f"{matchResult[0].text.strip()} - {matchResult[1].text.strip()}"

                #get match time
                matchtime = allMatches[i].find("div",{"class":"MResult"}).find("span",{"class":"time"}).text.strip()

                #add match info to matchDetails
                matchDetails.append({"نوع البطولة": championshipTilte,
                    "الفريق الأول": teamA,
                    "الفريق الثاني": teamB,
                    "موعد المباراة": matchtime,           
                    "النتيجة": score
                })

        for i in range(len(championships)):
            getMatchInfo(championships[i])

        ####save match info into csv file####
        try:
            #get header of file 
            keys = matchDetails[0].keys()

            with open("matchDetails.csv","w") as csvfile:
                dictWriter = csv.DictWriter(csvfile,keys) 
                dictWriter.writeheader()
                dictWriter.writerows(matchDetails)
        except IndexError:
            print("There are no matches on this date")         

    main(page)