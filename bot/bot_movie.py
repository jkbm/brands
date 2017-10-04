import requests
import json
payload = {'api_key' : 'bb18f8d3d31f7eb5cc97e4fd4bf3832b'}

'''
res = requests.get('https://api.themoviedb.org/3/authentication/token/new', params = payload)
data = res.json()

payload['request_token'] = data['request_token']
payload['username'] = 'jekabm'
payload['password'] = '159951'

print payload['request_token']

res1 = requests.get('https://api.themoviedb.org/3/authentication/token/validate_with_login', params = payload)
print res1.status_code


res2 = requests.get('https://api.themoviedb.org/3/authentication/session/new', params = payload)
jres2 = res2.json()
payload['session_id'] = jres2['session_id']
print res2.json()
'''
def getMovie(search_q):
    search_url = 'https://api.themoviedb.org/3/search/movie?api_key={0}&query={1}'.format(payload['api_key'], search_q)
    search = requests.get(search_url)
    jsearch = search.json()
    try:
        ret = jsearch['results'][0]
    except IndexError:
        print "RESPONSE!!!!!!!!!!: " + str(jsearch)
        ret = {'title': 'There is no such movie in our database.', 'release_date':'_______', 'overview':'Unfortunately, no info on this movie', 'poster_path' : "/lZpWprJqbIFpEV5uoHfoK0KCnTW.jpg"}

    return ret

