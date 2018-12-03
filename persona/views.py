import json
import requests

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Track, User

def redirect_view(request):
    r = redirect('https://accounts.spotify.com/authorize?client_id=a4c7fa479a3e48bc95a742faa8485e0c&response_type=code&redirect_uri=http://127.0.0.1:8000/persona/app/&scope=user-read-private%20playlist-read-private%20playlist-read-collaborative%20user-top-read%20user-read-recently-played&state=34fFs29kd09&show_dialog=true')
    print(r.status_code)
    return r

def home_view(request):
    context = { 'text': 'Hello!' }
    return render(request, 'persona/index.html', context)

def app(request):
    client_id = 'a4c7fa479a3e48bc95a742faa8485e0c'
    client_secret = 'bb1e58662dfc49d398a81896acf59282'
    try:
        data = request.GET['code']
    except (KeyError):
        return render(request, 'persona/app.html', data)
    else:
        headers = {
            'Authorization':'Basic YTRjN2ZhNDc5YTNlNDhiYzk1YTc0MmZhYTg0ODVlMGM6YmIxZTU4NjYyZGZjNDlkMzk4YTgxODk2YWNmNTkyODI='
        }
        code = data
        params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/persona/app/'
        }
        r = requests.post('https://accounts.spotify.com/api/token', data = params, headers = headers)
        jdata = r.json()
        print(jdata)
        token = jdata["access_token"]

        headers = {'Authorization': 'Bearer ' + token}
        params = {
            'limit': 50
        }
        index = 0
        all_playlists = {}
        playlists = (requests.get('https://api.spotify.com/v1/me/playlists', params = params, headers = headers)).json()
        all_playlists[index] = playlists
        index += 1
        while (playlists["next"]) :
            playlists = (requests.get(playlists["next"], headers = headers)).json()
            all_playlists[index] = [playlists]
            index += 1

        other_count = 0
        count = 0
        popularity = 0
        explicit = 0
        outer_index = 0
        inner_index = 0

        all_features = {}
        all_tracklist = {}
        for z in all_playlists:
            for x in all_playlists[z]["items"]:
                tracklist = x["href"]
                count += x["tracks"]["total"]
                fields = "?fields=items(added_at,is_local,track(name,id,popularity,explicit,album(id),artists(id))),next&limit=100"
                tracklist += "/tracks" + fields
                tracklist = (requests.get(tracklist, headers = headers)).json()
                all_tracklist[outer_index] = tracklist
                outer_index += 1
                while(tracklist["next"]) :
                    tracklist = (requests.get(tracklist["next"] + "&fields=items(added_at,is_local,track(name,id,popularity,explicit,album(id),artists(id))),next", headers = headers)).json()
                    all_tracklist[outer_index] = tracklist
                    outer_index += 1

                max = 0
                artist_max = 0
                features = 'https://api.spotify.com/v1/audio-features?ids='
                genres = 'https://api.spotify.com/v1/artists?ids='
        for b in all_tracklist:
            features = 'https://api.spotify.com/v1/audio-features?ids='
            for y in all_tracklist[b]["items"]:
                if (not(y["is_local"])):
                    popularity += y["track"]["popularity"]
                    if(y["track"]["explicit"]):
                        explicit += 1
                    features += y["track"]["id"]
                    features += ","
                    max += 1

                    if (max == 100):
                        features = features[0:-1]
                        features = (requests.get(features, headers = headers)).json()
                        all_features[inner_index] = features
                        features = 'https://api.spotify.com/v1/audio-features?ids='
                        max = 0
                        inner_index += 1

                else:
                    count -= 1



            features = features[0:-1]
            features = (requests.get(features, headers = headers)).json()
            all_features[inner_index] = features
            inner_index += 1

        danceability = 0
        energy = 0
        key = {
        0:0,
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0,
        11:0
        }
        loudness = 0
        major = 0
        minor = 0
        speechiness = 0
        acousticness = 0
        instrumentalness = 0
        liveness = 0
        valence = 0
        tempo = 0
        time_signature = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
            9:0
        }
        duration = 0

        for y in all_features:
            for x in all_features[y]["audio_features"]:
                if (x != None):
                    danceability += x["danceability"]
                    energy += x["energy"]
                    loudness += x["loudness"]
                    if (x["mode"]):
                        major += 1
                    else:
                        minor += 1
                    speechiness += x["speechiness"]
                    acousticness += x["acousticness"]
                    if (x["instrumentalness"] > 0.5):
                        instrumentalness += 1
                    if (x["liveness"] > 0.8):
                        liveness += 1
                    valence += x["valence"]
                    tempo += x["tempo"]
                    duration += x["duration_ms"]
                    key[x["key"]] += 1
                    if (x["time_signature"] != 0):
                        time_signature[x["time_signature"]] += 1

        com = 0
        com_val = key[0]
        c = round(key[0] * 100 / count, 2)
        cs = round(key[1] * 100 / count, 2)
        d = round(key[2] * 100 / count, 2)
        ds = round(key[3] * 100 / count, 2)
        e = round(key[4] * 100 / count, 2)
        f = round(key[5] * 100 / count, 2)
        fs = round(key[6] * 100 / count, 2)
        g = round(key[7] * 100 / count, 2)
        gs = round(key[8] * 100 / count, 2)
        a = round(key[9] * 100 / count, 2)
        bf = round(key[10] * 100 / count, 2)
        b = round(key[11] * 100 / count, 2)
        for x in key:
            if (key[x] > com_val):
                com = x
                com_val = key[x]

        key = com
        key_times = com_val

        com = 1
        com_val = time_signature[1]
        for x in time_signature:
            if (time_signature[x] > com_val):
                com = x
                com_val = time_signature[x]

        time_signature = com
        signature_times = com_val

        danceability /= count
        energy /= count
        loudness /= count
        major /= count
        minor /= count
        speechiness /= count
        acousticness /= count
        instrumentalness /= count
        liveness /= count
        valence /= count
        tempo /= count
        duration /= count
        popularity /= count
        explicit /= count
        if (major > minor):
            mode = 'Major'
        else:
            mode = 'Minor'

        if (key == 0):
            key = 'C'
        elif (key == 1):
            key = 'C#/D♭'
        elif (key == 2):
            key = 'D'
        elif (key == 3):
            key = 'D#/E♭'
        elif (key == 4):
            key = 'E'
        elif (key == 5):
            key = 'F'
        elif (key == 6):
            key = 'F#/G♭'
        elif (key == 7):
            key = 'G'
        elif (key == 8):
            key = 'G#/A♭'
        elif (key == 9):
            key = 'A'
        elif (key == 10):
            key = 'A#/B♭'
        elif (key == 11):
            key = 'B'

        instrumentalness = round(instrumentalness * 100, 2)
        liveness = round(liveness * 100, 2)
        valence = round(valence, 2)
        tempo = round(tempo, 2)
        popularity = round(popularity, 2)
        explicit = round(explicit * 100, 2)
        valence = round(valence)
        loudness_p = (60 + loudness) * 100 / 60
        loudness = round(loudness, 2)

        endpoint = 'https://api.spotify.com/v1/me/top/tracks?limit=50'
        audio_end = 'https://api.spotify.com/v1/audio-features?ids='

        def check(x, y, z):
            if x > z and y > z:
                return 1
            elif x <= z and y <= z:
                return 1
            else:
                return 0

        dance_pr = None
        energy_pr = None
        loud_pr = None
        speech_pr = None
        acoust_pr = None

        def not_taken(id):
            return id != dance_pr and id != energy_pr and id != loud_pr and id != speech_pr and id != acoust_pr

        top = (requests.get(endpoint, headers = headers)).json()
        for x in top["items"]:
            audio_end += x["id"]
            audio_end += ','
        top_audio = (requests.get(audio_end, headers = headers)).json()
        #while (dance_pr == None or energy_pr == None or loud_pr == None or speech_pr == None or acoust_pr == None):
        for x in top_audio["audio_features"]:
            if (check(danceability, x["danceability"], 0.5)):
                if (not_taken(x["id"]) and dance_pr == None):
                    dance_pr = x["id"]
            if (check(energy, x["energy"], 0.5)):
                if (not_taken(x["id"]) and energy_pr == None):
                    energy_pr = x["id"]
            if (check(loudness, x["loudness"], -30)):
                if (not_taken(x["id"]) and loud_pr == None):
                    loud_pr = x["id"]
            if (speechiness < 0.33 and x["speechiness"] < 0.33):
                if (not_taken(x["id"]) and speech_pr == None):
                    speech_pr = x["id"]
            elif ((speechiness >= 0.33 and speechiness < 0.66) and (x["speechiness"] >= 0.33 and x["speechiness"] < 0.66)):
                if (not_taken(x["id"]) and speech_pr == None):
                    speech_pr = x["id"]
            elif (speechiness >= 0.66 and x["speechiness"] >= 0.66):
                if (not_taken(x["id"]) and speech_pr == None):
                    speech_pr = x["id"]
            if (check(acousticness, x["acousticness"], 0.5)):
                if (not_taken(x["id"]) and acoust_pr == None):
                    acoust_pr = x["id"]

        endpoint = 'https://api.spotify.com/v1/tracks?ids=' + dance_pr + ',' + energy_pr + ',' + loud_pr + ',' + speech_pr + ',' + acoust_pr
        top = (requests.get(endpoint, headers = headers)).json()
        dance_pr = top["tracks"][0]["preview_url"]
        dance_name = top["tracks"][0]["name"]
        dance_img = top["tracks"][0]["album"]["images"][0]["url"]

        energy_pr = top["tracks"][1]["preview_url"]
        energy_name = top["tracks"][1]["name"]
        energy_img = top["tracks"][1]["album"]["images"][0]["url"]

        loud_pr = top["tracks"][2]["preview_url"]
        loud_name = top["tracks"][2]["name"]
        loud_img = top["tracks"][2]["album"]["images"][0]["url"]

        speech_pr = top["tracks"][3]["preview_url"]
        speech_name = top["tracks"][3]["name"]
        speech_img = top["tracks"][3]["album"]["images"][0]["url"]

        acoust_pr = top["tracks"][4]["preview_url"]
        acoust_name = top["tracks"][4]["name"]
        acoust_img = top["tracks"][4]["album"]["images"][0]["url"]

        context = {
            'dance_pr': dance_pr,
            'dance_name': dance_name,
            'dance_img': dance_img,
            'energy_pr': energy_pr,
            'energy_name': energy_name,
            'energy_img': energy_img,
            'loud_pr': loud_pr,
            'loud_name': loud_name,
            'loud_img': loud_img,
            'speech_pr': speech_pr,
            'speech_name': speech_name,
            'speech_img': speech_img,
            'acoust_pr': acoust_pr,
            'acoust_name': acoust_name,
            'acoust_img': acoust_img,
            'danceability': danceability * 100,
            'energy': energy * 100,
            'loudness': loudness,
            'loudness_p': loudness_p,
            'major': major,
            'minor': minor,
            'mode': mode,
            'speechiness': speechiness * 100,
            'acousticness': acousticness * 100,
            'instrumentalness': instrumentalness,
            'liveness': liveness,
            'valence': valence,
            'tempo': tempo,
            'duration': duration,
            'count': count,
            'key': key,
            'time_signature': time_signature,
            'popularity': popularity,
            'explicit': explicit,
            'c': c,
            'cs': cs,
            'd': d,
            'ds': ds,
            'e': e,
            'f': f,
            'fs': fs,
            'g': g,
            'gs': gs,
            'a': a,
            'bf': bf,
            'b': b
        }

    return render(request, 'persona/app.html', context)
