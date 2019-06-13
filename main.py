from flask import Flask, request, render_template
from octopus import Octopus
import json, requests, flask


def obtener_id(self, url):
    for j in url:
        if j.isdigit():
            try:
                sig = str(self.obtener_id(url[url.find(j)+1:]))
                if sig != "None":
                    digit = str(j) + sig
                    return digit
                else:
                    return str(j)
            except IndexError:
                pass
        else:
            pass

def personajes(personajes):
    for personaje in personajes:
        pass


app = Flask(__name__)

'''1. Página principal: Se deben listar todas las películas de la saga, con su nombre, año
de lanzamiento, director y productor(es), y número de episodio. Cada película debe dar
la opción de ver más información respecto a esta misma.'''
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        return busqueda
    else:
        url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
        req = {"query": "{allFilms {films{title releaseDate producers openingCrawl director episodeID characterConnection {characters {name}} planetConnection {planets {name}} starshipConnection {starships {name}} vehicleConnection {vehicles {name}} speciesConnection {species {name}} created edited }}}"}
        films = requests.post(url=url, json=req).json()["data"]["allFilms"]["films"]
        return render_template('index.html', result = films)

'''2. Al hacer click en una película, se debe mostrar una nueva página con toda la información
que entrega la API relacionada a la película, filtrando la información de vehículos y
especies'''
@app.route("/peliculas/<pid>")
def peliculas(pid = None):
    url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
    img = "../static/images/img{}.jpg".format(pid)
    dic_id = {"1": "4", "2": "5", "3": "6", "4": "1", "5": "2", "6": "3"}
    pid = dic_id[pid]
    pelicula = "film(filmID:{})".format(pid)
    req = {"query":"{" + pelicula + " {title releaseDate openingCrawl producers director episodeID characterConnection {characters {name id}} planetConnection {planets {name id}} starshipConnection {starships {name id}} created edited }}"}
    film = requests.post(url=url, json=req).json()["data"]["film"]
    return render_template('pelicula.html', result = film, personajes = film["characterConnection"]["characters"], naves =  film["starshipConnection"]["starships"], planetas = film["planetConnection"]["planets"],img=img)

@app.route("/personajes/<pid>")
def personajes(pid = None):
    url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
    personaje = "person(id:\"{}\")".format(pid)
    req = {"query": "{" + personaje + "{name height mass filmConnection {films {title episodeID}} eyeColor hairColor birthYear skinColor starshipConnection {starships {name id}} homeworld {name id} gender}}"}
    character = requests.post(url=url, json=req).json()["data"]["person"]
    return render_template('personaje.html', result = character, peliculas = character["filmConnection"]["films"], naves = character["starshipConnection"]["starships"])

@app.route("/planetas/<pid>")
def planetas(pid = None):
    url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
    planeta = "planet(id:\"{}\")".format(pid)
    req = {"query": "{" + planeta + "{name id orbitalPeriod  filmConnection{films {title episodeID}} rotationPeriod gravity climates terrains surfaceWater population residentConnection {residents {name id}} }}"}
    planet = requests.post(url=url, json=req).json()["data"]["planet"]
    return render_template('planeta.html', result = planet, peliculas = planet["filmConnection"]["films"], residentes = planet["residentConnection"]["residents"])

@app.route("/naves/<pid>")
def naves(pid = None):
    url =  "https://swapi-graphql-integracion-t3.herokuapp.com/"
    nave = "starship(id:\"{}\")".format(pid)
    req = {"query": "{" + nave + "{name model manufacturers maxAtmospheringSpeed cargoCapacity crew hyperdriveRating MGLT costInCredits length starshipClass filmConnection{films {title episodeID}} pilotConnection{pilots {name id}} }}"}
    starship = requests.post(url=url, json=req).json()["data"]["starship"]
    return render_template('nave.html', result = starship, peliculas = starship["filmConnection"]["films"], pilotos = starship["pilotConnection"]["pilots"])
