import os
from twilio.rest import Client
from datetime import datetime
import schedule
import time
import random

# send good morning texts to your significant loved ones
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

# send league messages to your friend. Remind them to get on!
LEAGUE_MESSAGES = ["eyyyyy you wanna duo queue?",
                   "What's up baus",
                   "Let's party with rift herald",
                   "Road to Challenger??",
                   "Hey Baus. Wanna hop on league?",
                   "Summoner's rift time?",
                   "Ready to pop off in league?",
                   "Hey baby let's explore the jungle together"]


def send_message(messages: list, twilio_number: str, recipient_number: str):
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
    # randomizes which message from the list you send to a person.
    string = messages[random.randint(0, len(messages) - 1)]

    # Enter the twilio phone number you are using and the phone number you are messaging to.
    message = client.messages \
        .create(
        body=string,
        from_=twilio_number,
        to=recipient_number
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


"""
Allows you to automate the task of sending text messages using schedule.
Sends one message at 9:00 AM and another message at 4:00 PM.
Remember that the function send_message has 3 parameters: messages, twilio_number, recipient_number.
Sample twilio_number = '+12518920091'
sample recipient_number = '+19496338213'
"""
# sample phone numbers include "+19498234109"

schedule.every().day.at("09:00").do(send_message, MORNING_MESSAGES, 'twilio_number', 'recipient_number')
# prints out which morning message you sent
schedule.every().day.at("09:00").do(message_sent)
schedule.every().day.at("16:00").do(send_message, LEAGUE_MESSAGES, 'twilio_number', 'recipient_number')
# prints out which league messages you sent
schedule.every().day.at("16:00").do(message_sent)

if __name__ == "__main__":
    receive_message()

    while True:
        schedule.run_pending()
        time.sleep(1)
