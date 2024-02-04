import requests
import csv
import re
def getMovieById(id):
    params = {'apikey':'9a2d82b8', 'i':id}
    movie = requests.get('https://www.omdbapi.com/', params)
    awardWins = 0
    awardNominations = 0
    try:
        awardWins = re.findall("[0-9]+ wins", movie.json()['Awards'])[0].split(" ")[0]
    except:
        print('No Wins')
    try: 
        awardNominations = re.findall("[0-9]+ nominations", movie.json()['Awards'])[0].split(" ")[0]
    except:
        print('No Nominations')
         
    runTime = re.findall("[0-9]+ min", movie.json()['Runtime'])[0].split(" ")[0]
    boxOfficeCleaned = ''
    for i in range(len(movie.json()['BoxOffice'])):
         if movie.json()['BoxOffice'][i] not in ('$',','):
              boxOfficeCleaned += movie.json()['BoxOffice'][i]
    
    return {
         'Title':f"{movie.json()['Title']}",
         'Director':f"{movie.json()['Director']}",
         'Country':f"{movie.json()['Country']}",
         'Metascore':f"{movie.json()['Metascore']}",
         'Runtime':f"{runTime}",
         'Genre':f"{movie.json()['Genre']}",
         'Award Wins':f"{awardWins}", 
         'Award Nominations':f"{awardNominations}", 
         'Box Office': f"{boxOfficeCleaned}"
         }
oscarWinners = []
with open("./oscar_winners.csv") as csvfile:
        movieReader = csv.reader(csvfile, delimiter=",")
        rows = list(movieReader)
        for i in range(1,len(rows)):
            movieId = rows[i][1]
            oscarWinners.append(getMovieById(movieId))

with open('movies.csv', 'w', newline='') as csvfile:
    fieldnames = ['Title', 'Runtime', 'Director','Country','Metascore','Genre', 'Award Wins', 'Award Nominations', 'Box Office']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for each in oscarWinners:
         writer.writerow(each)