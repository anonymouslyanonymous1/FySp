from flask import Flask, flash, redirect, render_template, request, session
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    api_key = ""
    choice = request.args.get("choice", default="movie")
    if choice == 'movie':
        movie_name = request.args.get("title", default="bcnrSIxJxi") #<- Random strings
        api = "https://api.themoviedb.org/3/search/movie?api_key="+ api_key +"&query="+ movie_name
    else:
        tv_name = request.args.get("title", default="bcnrSIxJxi")
        api1 = "https://api.themoviedb.org/3/search/tv?api_key="+ api_key +"&query="+ tv_name
    if choice == "movie":
        movie_info = requests.get(api).json()
        posters = []
        overviews = []
        ids = []
        titles = []
        movies = len(movie_info['results'])
        searched = True
        i = 0
        try:
            if  movies >= 1:
                for i in range(movies):
                    movie_title = movie_info['results'][i]['title']
                    id = movie_info['results'][i]['id']
                    poster_path = movie_info['results'][i]['poster_path']
                    overview = movie_info['results'][i]['overview']
                    movie_id = id
                    request2 = "https://api.themoviedb.org/3/movie/"+ str(movie_id) +"/watch/providers?api_key="+ api_key
                    streamer_info = requests.get(request2).json()
                    request3 = "https://api.themoviedb.org/3/configuration/countries?api_key="+ api_key
                    iso_regions = requests.get(request3).json()
                    iso = []
                    ok1 = None
                    provider = None
                    logo = None
                    for i in range(len(iso_regions)):
                        iso1 = iso_regions[i]['iso_3166_1']
                        iso.append(iso1)

                    for i in range(len(iso)):
                        try:
                            streamer1 = streamer_info['results'][iso[i]]['flatrate'][0]['provider_name']
                            if streamer1 in ('Netflix', 'Amazon Prime Video', 'Disney Plus'):
                                provider = streamer_info['results'][iso[i]]['flatrate'][0]['provider_name']
                                logo = streamer_info['results'][iso[i]]['flatrate'][0]['logo_path']
                                break
                            else:
                                ok1 = False
                        except:
                            ok1 = False
                            continue
                    #Adding to array
                    titles.append(movie_title)
                    if str(logo) != "None":
                        provider_img="https://image.tmdb.org/t/p/w500" +  str(logo)
                    else:
                        provider_img="../static/svg.svg"
                    ids.append(provider_img)
                    posters.append("https://image.tmdb.org/t/p/w500"+ str(poster_path))
                    overviews.append(overview)
                    

                    i += 1
                    # , title=titles, poster=posters, summary=overviews, id = ids
                return render_template("index.html", movies=movies, title=titles, poster=posters, summary=overviews, id = ids)
            else:
                movie_title = movie_info['results'][0]['title']
                id = movie_info['results'][0]['id']
                poster_path = movie_info['results'][i]['poster_path']
                overview = movie_info['results'][i]['overview']
                return render_template("index.html", title= movie_title, poster="https://image.tmdb.org/t/p/w500"+ str(poster_path), summary=overview, id=id, ok = True)

        except:
            return render_template("index.html", error=True)
    if choice == "web":
        tv_info = requests.get(api1).json()
        posters = []
        overviews = []
        ids = []
        titles = []
        tvs = len(tv_info['results'])
        i = 0
        try:
            if  tvs >= 1:
                for i in range(tvs):
                    tv_title = tv_info['results'][i]['name']
                    id = tv_info['results'][i]['id']
                    poster_path = tv_info['results'][i]['poster_path']
                    overview = tv_info['results'][i]['overview']
                    request2 = "https://api.themoviedb.org/3/tv/"+ str(id) +"/watch/providers?api_key="+ api_key
                    streamer_info = requests.get(request2).json()
                    request3 = "https://api.themoviedb.org/3/configuration/countries?api_key="+ api_key
                    iso_regions = requests.get(request3).json()
                    iso = []
                    ok1 = None
                    provider = None
                    logo = None
                    for i in range(len(iso_regions)):
                        iso1 = iso_regions[i]['iso_3166_1']
                        iso.append(iso1)

                    for i in range(len(iso)):
                        try:
                            streamer1 = streamer_info['results'][iso[i]]['flatrate'][0]['provider_name']
                            if streamer1 in ('Netflix', 'Amazon Prime Video', 'Disney Plus'):
                                provider = streamer_info['results'][iso[i]]['flatrate'][0]['provider_name']
                                logo = streamer_info['results'][iso[i]]['flatrate'][0]['logo_path']
                                break
                            else:
                                ok1 = False
                        except:
                            ok1 = False
                            continue
                    #Adding to array
                    titles.append(tv_title)
                    if str(logo) != "None":
                        provider_img="https://image.tmdb.org/t/p/w500" +  str(logo)
                    else:
                        provider_img="../static/svg.svg"
                    ids.append(provider_img)
                    posters.append("https://image.tmdb.org/t/p/w500"+ str(poster_path))
                    overviews.append(overview)

                    i += 1
                    # , title=titles, poster=posters, summary=overviews, id = ids
                return render_template("index.html", movies=tvs, title=titles, poster=posters, summary=overviews, id = ids)
            else:
                tv_title = tv_info['results'][0]['name']
                id = tv_info['results'][0]['id']
                poster_path = tv_info['results'][i]['poster_path']
                overview = tv_info['results'][i]['overview']
                return render_template("index.html", title= tv_title, poster="https://image.tmdb.org/t/p/w500"+ str(poster_path), summary=overview, id=id, ok = True)

        except:
            return render_template("index.html", error=True)
app.run()