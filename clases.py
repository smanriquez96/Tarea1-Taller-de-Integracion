import requests, json

pid = 4
url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
pelicula = "film(filmID:{})".format(pid)
req = {"query":"{" + pelicula + " {title releaseDate openingCrawl producers director episodeID characterConnection {characters {name ID}} planetConnection {planets {name}} starshipConnection {starships {name}} created edited }}"}
film = requests.post(url=url, json=req).json()["data"]["film"]

print(film)
