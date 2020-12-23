import os
from twilio.rest import Client
from datetime import datetime
import schedule
import time
import random

MESSAGE_JAYDEN = ["Hey BB wanna go smoke?", "Why you looking extra cute today"]
MORNING_MESSAGES = ["Hey baby. I hope you had a nice morning <3",
                    "Good Morning you sexy beast",
                    "GIMORI",
                    "좋은 아침!",
                    "Good morning DADDY",
                    "Last night, I didn’t count sheep, I counted blessings. But they all pale in comparison to you. "
                    "I’m blessed to have you in my life.",
                    "It may be raining outside, but your love is keeping me warm.",
                    "Good morning, baby. You were with me in my dreams all night.",
                    "Good morning, sunshine. You’re the reason I wake up each morning.",
                    "Yesterday has gone. Morning has begun. Now it’s time to wake up and give me a hug. 🙂",
                    "Your smile is the only inspiration I need. Your love, the only motivation. You are my happiness.",
                    "Each morning I open my eyes, all I want to see is you.",
                    "I still can’t believe you took me. I’m the luckiest guy in the world.",
                    "I can’t get you out of my mind. Then again, I wouldn’t know. I’ve never tried to get you out.",
                    "You are my guiding star. Without you, I’d be lost in a dark, cold world.",
                    "I don’t know what gets me more excited: the thought of meeting you in a few hours, or the dream I"
                    " had of you last night",
                    "The light that shines from you is more vital to me than the sunlight in the morning. "
                    "Rise and shine, my beautiful queen."]

LEAGUE_MESSAGES = ["eyyyyy you wanna duo queue?",
                   "Hey Baus. Wanna hop on league?",
                   "Summoner's rift time?",
                   "Ready to pop off in league?",
                   "Hey baby let's explore the jungle together"]


def send_message(messages: list):
    """
    Sends a message to a phone number of your choosing. Since we are using the free trial version of Twilio,
    we can only send messages to verified phone numbers
    :param messages: list
    :return: None
    """
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    string = messages[random.randint(0, len(messages) - 1)]

    message = client.messages \
        .create(
        body=string,
        from_='+12518664402',
        to='+19499336399'
    )


def message_sent():
    """
    Retrieves the latest message that was sent or received from the twilio phone number.
    This function will be used to see which message was sent when you send a message to someone.
    :return: None
    """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages.list(limit=1)
    for record in message:
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Message sent at:", current_time)
        print("Message sent from ", record.from_, " to ", record.to, "\nBody: ", record.body, sep="", end="\n\n")


def receive_message():
    """
    Reveives the latest 20 messages sent from the twilio phone number
    :return:None
    """
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    messages = client.messages.list(limit=20)
    i = 1
    print("\nHere are your latest", len(messages), "messages!")
    for record in messages:
        print("Message ", i, ": Sent from ", record.from_, " to ", record.to, "\nBody: ", record.body, sep="",
              end="\n\n")
        i += 1


schedule.every().day.at("09:00").do(send_message, MORNING_MESSAGES)
# prints out which morning message you sent
schedule.every().day.at("09:00").do(message_sent)
schedule.every().day.at("12:58").do(send_message, LEAGUE_MESSAGES)
# prints out which league messages you sent
schedule.every().day.at("12:58").do(message_sent)

if __name__ == "__main__":
    receive_message()

    while True:
        schedule.run_pending()
        time.sleep(1)
