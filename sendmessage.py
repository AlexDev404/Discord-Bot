import json
import requests
import string
import random
import time

# SET RAIDMODE ON OR OFF

RAIDMODE = False


def retMode():
    if RAIDMODE:
        return "ON"
    else:
        return "OFF"


print("DISCORD MESSAGE SENDER v1.0")
print("RAIDMODE IS: " + retMode() + "\n")

authToken = input("ENTER DISCORD AUTHORIZATION TOKEN: ")
if not authToken:
    print("SERVER: NO TOKEN: UNAUTHORIZED")
    exit(-1)

message = input("TYPE MESSAGE: ")

# EMBED REFERENCE FROM: https://discord.com/developers/docs/resources/channel#embed-object
# ICON USED: https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png
# VIDEO USED: https://www.youtube.com/watch?v=jn9TqFUyWiM

embed = [
    {
        "title": "Title",
        "type": "rich",
        "description": "Body",
      #  "url": "https://example.com",
        "author": {
            "name": "Test",
            "url": "https://example.com",
            "icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "proxy_icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png"

        },
        "fields": [
            {
                "name": "Test Field",
                "value": "Placeholder",
                "inline": "false",
            }
        ],
        "provider": {
            "name": "Provider Name",
            "url": "https://example.com"
        },
        "video": {
            "url": "https://www.youtube.com/watch?v=jn9TqFUyWiM",
            "proxy_url": "https://www.youtube.com/watch?v=jn9TqFUyWiM",
            "height": 900,
            "width": 900,
        },
        "image": {
            "url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "proxy_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "height": 900,
            "width": 900
        },
        "thumbnail": {
            "url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "proxy_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "height": 500,
            "width": 500
        },
        "footer": {
            "text": "FOOTER TEXT",
            "icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
            "proxy_icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png"
        },
        "color": 0x0400ff,
    }
]
components = [
    {
        "type": 1,
        "components": [
            {
                "type": 2,
                "style": 5,
                "label": "More information",
                "url": "https://rythm.fm/"
            },
            {
                "type": 2,
                "style": 1,
                "label": "Sign up for Rythm newsletter",
                "custom_id": "newsletter-signup",
                "hash": ""
            },
            {
                "type": 2,
                "style": 5,
                "label": "Support us on Patreon",
                "url": "https://patreon.com/rythm"
            }
        ]
    }
]


# tts = input("TTS? (true OR false): ")


def id_generator(size=17, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def genBody(message, tts):
    body = {
        "content": message,
        "embeds": embed,
        #        "components": components,   - NOT WORKING
        "nonce": id_generator(17, "1234567890"),
        "tts": tts
    }
    return body


headers_ = {
    "accept": "*/*",
    "accept-language": "en-US",
    "authorization": str(authToken),
    "content-type": "application/json",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

url_base = 'https://discord.com/api/v9/channels/'
url_id = input("CHANNEL ID: ")
url = "".join(url_base + url_id + "/messages")
print(url)


# Use the 'headers' parameter to set the HTTPS headers:
# bodyjson = json.dumps(genBody())

# print(bodyjson) -- DEBUG

def sendMessage():
    bodyjson = json.dumps(genBody(message, "false"))
    res = requests.post(url, data=bodyjson, headers=headers_)
    resjson = json.loads(res.text)

    try:
        print("SERVER: " + resjson["message"])
        try:
            print(" - RETRY AFTER: " + str(resjson["retry_after"]) + "s\n")
        except KeyError or TypeError:
            pass
    except KeyError or TypeError:
        print("Sent!\n")
        print("Message Sent: ")
        print(resjson["content"] + "\n")
        print("Sent as: ")
        print(resjson["author"]["username"] + "#" + resjson["author"]["discriminator"] + "\n")

    # print(bodyjson)
    # print(resjson)
    time.sleep(0.05)


while RAIDMODE:
    sendMessage()

sendMessage()
