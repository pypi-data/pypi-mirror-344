import httpx

# From nekosbest.py
def lurk():
    response = httpx.get('https://nekos.best/api/v2/lurk')
    return response.json()['results'][0]['url']

def shoot():
    response = httpx.get('https://nekos.best/api/v2/shoot')
    return response.json()['results'][0]['url']

def sleep():
    response = httpx.get('https://nekos.best/api/v2/sleep')
    return response.json()['results'][0]['url']

def shrug():
    response = httpx.get('https://nekos.best/api/v2/shrug')
    return response.json()['results'][0]['url']

def stare():
    response = httpx.get('https://nekos.best/api/v2/stare')
    return response.json()['results'][0]['url']

def wave():
    response = httpx.get('https://nekos.best/api/v2/wave')
    return response.json()['results'][0]['url']

def poke():
    response = httpx.get('https://nekos.best/api/v2/poke')
    return response.json()['results'][0]['url']

def smile():
    response = httpx.get('https://nekos.best/api/v2/smile')
    return response.json()['results'][0]['url']

def peck():
    response = httpx.get('https://nekos.best/api/v2/peck')
    return response.json()['results'][0]['url']

def wink():
    response = httpx.get('https://nekos.best/api/v2/wink')
    return response.json()['results'][0]['url']

def blush():
    response = httpx.get('https://nekos.best/api/v2/blush')
    return response.json()['results'][0]['url']

def smug():
    response = httpx.get('https://nekos.best/api/v2/smug')
    return response.json()['results'][0]['url']

def tickle():
    response = httpx.get('https://nekos.best/api/v2/tickle')
    return response.json()['results'][0]['url']

def yeet():
    response = httpx.get('https://nekos.best/api/v2/yeet')
    return response.json()['results'][0]['url']

def think():
    response = httpx.get('https://nekos.best/api/v2/think')
    return response.json()['results'][0]['url']

def highfive():
    response = httpx.get('https://nekos.best/api/v2/highfive')
    return response.json()['results'][0]['url']

def feed():
    response = httpx.get('https://nekos.best/api/v2/feed')
    return response.json()['results'][0]['url']

def bite():
    response = httpx.get('https://nekos.best/api/v2/bite')
    return response.json()['results'][0]['url']

def bored():
    response = httpx.get('https://nekos.best/api/v2/bored')
    return response.json()['results'][0]['url']

def nom():
    response = httpx.get('https://nekos.best/api/v2/nom')
    return response.json()['results'][0]['url']

def yawn():
    response = httpx.get('https://nekos.best/api/v2/yawn')
    return response.json()['results'][0]['url']

def facepalm():
    response = httpx.get('https://nekos.best/api/v2/facepalm')
    return response.json()['results'][0]['url']

def cuddle():
    response = httpx.get('https://nekos.best/api/v2/cuddle')
    return response.json()['results'][0]['url']

def kick():
    response = httpx.get('https://nekos.best/api/v2/kick')
    return response.json()['results'][0]['url']

def happy():
    response = httpx.get('https://nekos.best/api/v2/happy')
    return response.json()['results'][0]['url']

def hug():
    response = httpx.get('https://nekos.best/api/v2/hug')
    return response.json()['results'][0]['url']

def baka():
    response = httpx.get('https://nekos.best/api/v2/baka')
    return response.json()['results'][0]['url']

def pat():
    response = httpx.get('https://nekos.best/api/v2/pat')
    return response.json()['results'][0]['url']

def angry():
    response = httpx.get('https://nekos.best/api/v2/angry')
    return response.json()['results'][0]['url']

def run():
    response = httpx.get('https://nekos.best/api/v2/run')
    return response.json()['results'][0]['url']

def nod():
    response = httpx.get('https://nekos.best/api/v2/nod')
    return response.json()['results'][0]['url']

def nope():
    response = httpx.get('https://nekos.best/api/v2/nope')
    return response.json()['results'][0]['url']

def kiss():
    response = httpx.get('https://nekos.best/api/v2/kiss')
    return response.json()['results'][0]['url']

def dance():
    response = httpx.get('https://nekos.best/api/v2/dance')
    return response.json()['results'][0]['url']

def punch():
    response = httpx.get('https://nekos.best/api/v2/punch')
    return response.json()['results'][0]['url']

def handshake():
    response = httpx.get('https://nekos.best/api/v2/handshake')
    return response.json()['results'][0]['url']

def slap():
    response = httpx.get('https://nekos.best/api/v2/slap')
    return response.json()['results'][0]['url']

def cry():
    response = httpx.get('https://nekos.best/api/v2/cry')
    return response.json()['results'][0]['url']

def pout():
    response = httpx.get('https://nekos.best/api/v2/pout')
    return response.json()['results'][0]['url']

def handhold():
    response = httpx.get('https://nekos.best/api/v2/handhold')
    return response.json()['results'][0]['url']

def thumbsup():
    response = httpx.get('https://nekos.best/api/v2/thumbsup')
    return response.json()['results'][0]['url']

def laugh():
    response = httpx.get('https://nekos.best/api/v2/laugh')
    return response.json()['results'][0]['url']

# From waifu_pics.py (skip functions with duplicate names)
def bully():
    response = httpx.get('https://api.waifu.pics/sfw/bully')
    return response.json()['url']

def lick():
    response = httpx.get('https://api.waifu.pics/sfw/lick')
    return response.json()['url']

def bonk():
    response = httpx.get('https://api.waifu.pics/sfw/bonk')
    return response.json()['url']

def glomp():
    response = httpx.get('https://api.waifu.pics/sfw/glomp')
    return response.json()['url']

def kill():
    response = httpx.get('https://api.waifu.pics/sfw/kill')
    return response.json()['url']

def cringe():
    response = httpx.get('https://api.waifu.pics/sfw/cringe')
    return response.json()['url']

# From nekoslife.py (skip functions with duplicate names)
def spank():
    response = httpx.get('https://nekos.life/api/v2/img/spank')
    return response.json()['url']
