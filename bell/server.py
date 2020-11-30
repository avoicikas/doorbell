from flask import Flask, render_template, request
import datetime
import raspM
import settings
import sys
from pymessenger import Bot

app = Flask(__name__)


# main page
@app.route("/")
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        "title": "HELLO!",
        "time": timeString,
        "bellSound": settings_new["ringRealBell"],
        "openDoors": settings_new["openDoors"],
    }
    return render_template("index.html", **templateData)


# facebook bot webhook verification
@app.route("/verify", methods=["GET"])
def verify():
    # webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get(
        "hub.challenge"
    ):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


# facebook bot webhook - respond to sender same text
@app.route("/verify", methods=["Post"])
def webhook():
    data = request.get_json()
    log(data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                # IDs
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]

                if messaging_event.get("message"):
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    elif "sticker_id" in messaging_event["message"]:
                        messaging_text = "sticker"
                    else:
                        messaging_text = "no text"

                    # Echo
                    if messaging_text == "o":
                        rasp.openDoors()
                        rasp.logger.debug("open from bot (o)")
                    if messaging_text == "O":
                        rasp.openDoors()
                        rasp.logger.debug("open from bot (O)")
                    if messaging_text == "sticker":
                        rasp.openDoors()
                        rasp.logger.debug("open from bot (sticker)")
                    if messaging_text == "Sound on":
                        settings_new["ringRealBell"] = 1
                    if messaging_text == "Sound off":
                        settings_new["ringRealBell"] = 0
                    response = settings_new["ringRealBell"]
                    bot.send_text_message(sender_id, response)
    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


# page button actions
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    if deviceName == "openDoors":
        if action == "on":
            settings_new["openDoors"] = 1
            rasp.openDoors()
            rasp.logger.debug("open from web button")
            settings_new["openDoors"] = 0
    if deviceName == "bellSound":
        if action == "on":
            settings_new["ringRealBell"] = 1
        if action == "off":
            settings_new["ringRealBell"] = 0
    templateData = {
        "title": "HELLO!",
        "time": timeString,
        "bellSound": settings_new["ringRealBell"],
        "openDoors": settings_new["openDoors"],
    }
    return render_template("index.html", **templateData)


if __name__ == "__main__":
    settings_new = settings.getSettings()  # load settings
    bot = Bot(settings_new["PAGE_ACCESS_TOKEN"])  # setup facebook bot
    rasp = raspM.raspModel(settings_new, bot)  # setup raspberry
    watcher = raspM.door_watcher(
        settings_new, rasp
    )  # setup function to monitor if someone is pressing doorbell
    watcher.daemon = True
    watcher.start()
    app.run(port=8000, host="0.0.0.0")  # run flask
