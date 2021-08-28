import praw
import random
import time

pc = False
test = False

app_name = ''
client_id = ''
client_secret = ''
username = ''
password = ''
user_agent = 'linux:appnaziv:v0.0.1 (by u/mojusername)'

subreddits = "binance+CryptoCurrency+Bitcoin+Crypto_General+cryptomining+CryptoMoonShots+investing"
millions_users = 23
website_url = 'https://joinpicoin.netlify.app'
max_karma_user = 777
sent_to_redditors_path = '/home/gillabo/Desktop/sent_to_redditors.txt' if pc else '/var/www/html/pi-reddit/sent_to_redditors.txt'
max_comments = 2000

if not pc: time.sleep(25)

def send_message(redditor):
    idn = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for x in range(4))
    subject = "Joinpicoin {0}".format(redditor.name)
    content = '''Pi Network is social coin with {0}M+ users on app stores. No catch, it costs $0 to mine (mint) them while we still can.
Read about its progress, ecosystem or other info here: {1} or simply ask me {2}. Join with my invite code if you wish: "gillabo".
Honestly, it's great crypto project and opportunity when the whitepaper is well studied. {3}.
Maybe you will thank me later for it. Sorry for the bother if not interested.'''.format(millions_users, website_url, redditor.name, idn)
    try:
        redditor.message(subject, content)
        return True
    except Exception as e:
        print("Failed to send message because:")
        print(e)
        return False

def redditor_eligible(redditor):
    try:
        return not redditor.is_employee and not redditor.is_mod and not redditor.is_gold and (redditor.comment_karma+redditor.link_karma)<max_karma_user and not(redditor.name in sent_to_redditors)
    except Exception as e:
        print(e)
        return False

def new_redditors(reddit, sent_to_redditors, subreddits):
    try:
        new_redditors = set([c.author for c in reddit.subreddit(subreddits).comments(limit=max_comments)]).difference(sent_to_redditors)
    except Exception as e:
        print(e)
        new_redditors = {}
        
    if len(new_redditors) == 0:
        time.sleep(10*60)
        return new_redditors(reddit, sent_to_redditors, subreddits)
    else:
        return new_redditors



reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)
sent = 0

while 1:
    with open(sent_to_redditors_path, 'r') as f:
        sent_to_redditors = set(f.read().split('\n'))
    next_redditors = new_redditors(reddit, sent_to_redditors, subreddits)
    time.sleep(2)
    
    for redditor in list(next_redditors):
        if redditor_eligible(redditor):
            if send_message(redditor):
                with open(sent_to_redditors_path, 'a') as f:
                    f.write('\n'+redditor.name)
                sent += 1; print("Message {0} sent to: {1}".format(sent, redditor.name))
                if sent%200 == 0:
                    sleep_for = random.randint(3*60, 5*60)
                    print("Wait {0} [s]".format(sleep_for))
                    time.sleep(sleep_for)
            sleep_for = random.randint(20, 24)
            print("Wait {0} [s]".format(sleep_for))
            time.sleep(sleep_for)
        else:
            time.sleep(2)
