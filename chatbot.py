import json
import requests
import string
import random
import time
import os
import aiml

embedMode = False
botname = "Bob Bot"
customColor = 0x001627  # Set to False if you want to use random values. Can use hex colors such as #001627 but instead
prefixed = False
lastresponse = " "


# of using a # use 0x in replacement of it


def retMode(mode):
    if mode:
        return "ON"
    else:
        return "OFF"


print("SIGN-IN TO ALICEBOT")
print("EMBED MODE IS " + str(retMode(embedMode)))
print("PREFIX MODE IS " + str(retMode(prefixed)))
authToken = input("ENTER DISCORD PERSONAL ACCESS TOKEN (Precede token with `Bot` if using a bot token): ")
if not authToken:
    print("SERVER: NO TOKEN: UNAUTHORIZED")
    exit(-1)


# tts = input("TTS? (true OR false): ")


def id_generator(size=17, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def genBody(message, tts):
    if embedMode:
        body = {
            "content": "",
            "embeds": [
                {
                    #  "title": "ALICEBOT TEST",
                    "type": "rich",
                    "description": message,
                    #  "url": "https://example.com",
                    "author": {
                        "name": botname,
                        "url": "https://github.com/AlexDev404/uDiscordAPI",
                        #  "icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png",
                        #  "proxy_icon_url": "https://cdn2.iconfinder.com/data/icons/search-engine-optimization-33/32/seo-06-512.png"

                    },
                    "color": customColor if customColor else id_generator(7, "1234567890")
                }
            ],

            "nonce": id_generator(17, "1234567890"),
            "tts": tts
        }
    else:
        body = {
            "content": message,
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
print("OUTPUT URL:" + url)

url_req = "".join(url_base + url_id + "/messages?limit=1")
print("INPUT URL: " + url_req)

url_getUser = "https://discord.com/api/v9/users/@me"


# Use the 'headers' parameter to set the HTTPS headers:
# bodyjson = json.dumps(genBody())

# print(bodyjson) -- DEBUG


def getUser():
    res = requests.get(url_getUser, data=None, headers=headers_)
    resjson = json.loads(res.text)

    try:
        print("SERVER: " + resjson["message"])
        try:
            print(" - RETRY AFTER: " + str(resjson["retry_after"]) + "s\n")
        except KeyError:
            pass
    except KeyError:
        pass

    # print(resjson["id"])
    return int(resjson["id"])


def sendMessage(message):
    bodyjson = json.dumps(genBody(message, "false"))
    ubodyjson = json.loads(bodyjson)

    # Don't let the bot reply to itself
    global lastresponse
    lastresponse = ubodyjson["content"]
    print(ubodyjson["content"])
    res = requests.post(url, data=bodyjson, headers=headers_)
    resjson = json.loads(res.text)

    try:
        print("SERVER: " + resjson["message"])
        try:
            print(" - RETRY AFTER: " + str(resjson["retry_after"]) + "s\n")
        except KeyError:
            pass
    except KeyError:
        #  print("Sent!\n")
        #  print("Message Sent: ")
        #  print(resjson["content"] + "\n")
        print("Sent as: ")
        print(resjson["author"]["username"] + "#" + resjson["author"]["discriminator"])

    # print(bodyjson)
    # print(resjson)
    # time.sleep(0.05)


def reqMessage():
    res = requests.get(url_req, data=None, headers=headers_)
    uresjson = json.loads(res.text)
    # resjson = json.dumps(uresjson, indent=3)

    try:
        print("SERVER: " + uresjson["message"])
        try:
            print(" - RETRY AFTER: " + str(uresjson["retry_after"]) + "s\n")
        except KeyError:
            pass
        except TypeError:
            pass
    except TypeError:
        x = 0
        while x < len(uresjson):
            if prefixed:
                if f"<@!{user_ID}>" in uresjson[x]["content"]:
                    # print("AHA!")
                    # print(uresjson[x]["content"])
                    inputtext = uresjson[x]["content"]
                    return inputtext
            else:
                # print(uresjson)
                inputtext = uresjson[x]["content"]
                return inputtext
            x = x + 1

    except KeyError:
        print("Seems that the bot has become disconnected. Shutting down...")
        return -1


# BOT CODE START

BRAIN_FILE = "brain.dump"

k = aiml.Kernel()

# To increase the startup speed of the bot it is
# possible to save the parsed aiml files as a
# dump. This code checks if a dump exists and
# otherwise loads the aiml from the xml files
# and saves the brain dump.
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
    print("Waiting for user input...")
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)
    print("Waiting for user input...")


# Endless loop which passes the input to the bot and prints
# its response


def main():
    # https://discord.com/api/v9/users/@me
    global user_ID
    user_ID = None

    if user_ID is not None:
        pass
    else:
        user_ID = int(getUser())

    # print("IN MAIN")
    # print(f"USERID = {user_ID}")

    # input_text = input("> ")
    botInput = reqMessage()

    # IF THE BOT IS NOT SUMMONED DO NOT RUN

    if botInput is "" or botInput is None or botInput == lastresponse:
        # pass
        # print("Waiting...")
        # Don't want to get banned from Discord for overwhelming their API for _Obvious_ reasons...
        time.sleep(5)
    else:
        if prefixed:
            if f"<@!{user_ID}>" in botInput:
                botInput = botInput.replace(f"<@!{user_ID}>", '')
                print(f"User says: {botInput}")
                response = k.respond(str(botInput))
                print(f"BOT SAYS: " + response)
                sendMessage(response)
                print("Waiting for user input...")
                time.sleep(7.5)
        else:
            print(f"User says: {botInput}")
            response = k.respond(str(botInput))
            print(f"BOT SAYS: " + response)
            sendMessage(response)
            print("Waiting for user input...")
            time.sleep(7.5)

    # KEEP CHECKIN'...

    main()


# KEEP CHECKIN'...


main()
