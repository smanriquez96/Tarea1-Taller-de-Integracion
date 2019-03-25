from flask import Flask, request, render_template
from octopus import Octopus
import json, requests, flask


###################################

class API:
    def __init__(self):
        self.datos = {}
        self.url =  "https://swapi.co"
        self.otto = Octopus (concurrency=8, auto_start=True, cache=True, expiration_in_seconds=10)

    def main(self):
        r = requests.get(self.url+"/api/films/")
        peliculas = r.json()
        peliculas = peliculas["results"]
        films = {}
        for i in peliculas:
            films[i["title"]] = i
        return films

    def filtro(self, dic):
        filtrados = {}
        for j in dic:
            if j != "vehicles" and j != "species":
                filtrados[j] = dic[j]
        return filtrados

    def films(self, id):
        r = requests.get(self.url+"/api/films/"+id)
        pelicula = r.json()
        pelicula = self.filtro(pelicula)
        return pelicula

    def people(self, id):
        r = requests.get(self.url+"/api/people/"+id)
        personaje = r.json()
        personaje = self.filtro(personaje)
        return personaje

    def planets(self, id):
        r = requests.get(self.url+"/api/planets/"+id)
        planeta = r.json()
        planeta = self.filtro(planeta)
        return planeta

    def starships(self, id):
        r = requests.get(self.url+"/api/starships/"+id)
        nave = r.json()
        nave = self.filtro(nave)
        return nave

    def obtener_nombres(self, url):
        r = requests.get(url)
        nombre = r.json()
        if "films" in url:
            return nombre["title"]
        else:
            return nombre["name"]

    def async_names(self, urls):
        otto = Octopus(concurrency=10, auto_start=True, cache=True,request_timeout_in_seconds = 10,
            expiration_in_seconds=20)
        nombres = {}
        def handle_url_response(url, response):
            response = json.loads(response.text)
            if "films" in url:
                id = self.obtener_id(url)
                nombres[id] = response["title"]

            else:
                id = self.obtener_id(url)
                nombres[id] = response["name"]

        for url in urls:
            otto.enqueue(url, handle_url_response)

        otto.wait()
        return nombres

    def async_search(self, s):
        urls = ["https://swapi.co/api/people/?search=","https://swapi.co/api/films/?search=",
        "https://swapi.co/api/planets/?search=","https://swapi.co/api/starships/?search="]
        urls = [url+s for url in urls]
        otto = Octopus(concurrency=10, auto_start=True, cache=True,request_timeout_in_seconds = 10,
            expiration_in_seconds=20)
        data = []
        def handle_url_response(url, response):
            response = json.loads(response.text)
            response = response["results"]
            for res in response:
                if "films" in res["url"]:
                    data.append([res["title"])

                else:
                    id = self.obtener_id(url)
                    data.append(res["name"])


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



####################################

app = Flask(__name__)
api = API()


@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        return busqueda
    else:
        results = api.main()
        return render_template('index.html', result = results, api =  api)

@app.route("/peliculas/<pid>")
def peliculas(pid = None):
    results = api.films(pid)
    personajes = api.async_names(results["characters"])
    planetas = api.async_names(results["planets"])
    naves = api.async_names(results["starships"])
    return render_template('pelicula.html', result = results, api = api, personajes = personajes, planetas = planetas, naves = naves)

@app.route("/personajes/<pid>")
def personajes(pid = None):
    results = api.people(pid)
    peliculas = api.async_names(results["films"])
    naves = api.async_names(results["starships"])
    return render_template('personaje.html', result = results, api = api, peliculas = peliculas, naves = naves)

@app.route("/planetas/<pid>")
def planetas(pid = None):
    results = api.planets(pid)
    peliculas = api.async_names(results["films"])
    residentes = api.async_names(results["residents"])
    return render_template('planeta.html', result = results, api = api, peliculas = peliculas, residentes = residentes)

@app.route("/naves/<pid>")
def naves(pid = None):
    results = api.starships(pid)
    peliculas = api.async_names(results["films"])
    pilotos = api.async_names(results["pilots"])
    return render_template('nave.html', result = results, api = api, peliculas = peliculas, pilotos = pilotos)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        data = api.async_search(busqueda)
        return render_template('busqueda.html', data = data)
