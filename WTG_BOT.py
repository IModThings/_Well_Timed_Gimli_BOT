import requests
import time
import json
import praw
from collections import deque
#https://api.pushshift.io/reddit/search/comment/?q=%22and%20my%20bow%22&q:not=%22axe%22&locked=%22false%22&over_18=%22false%22&size=100


def main():
    reddit = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='linux:com.WellTimedGimli:V0.1 (by I_Mod_Things)',
                     username='_Well_Timed_Gimli_')

    with open('replied_ids.txt', 'w+') as replied:
        replied_ids = deque(replied, maxlen=10)
        replied.close()

    while True:
        try:
            getPushshiftData(reddit, replied_ids)
        except:
            print("FAILED at getPushshiftData function call!")
        time.sleep(60)

def getPushshiftData(reddit,replied_ids):
    url = 'https://api.pushshift.io/reddit/search/comment/?q=%22and%20my%20bow%22&q:not=%22axe%22&locked=%22false%22&over_18=%22false%22&collapsed_because_crowd_control=%22false%22&size=5'
    #print(url)
    bow_comments = requests.get(url)
    pool = json.loads(bow_comments.text)
    replied_comments=[]
    for comment in pool["data"]:
        if comment["id"] in replied_ids:
            continue

        if len(comment["body"]) > 15:
            replied_ids.appendleft(comment["id"])
            continue

        if checkReplied(reddit,comment["id"])==True:
            replied_ids.appendleft(comment["id"])
            continue

        try:
            reddit.comment(id=comment['id']).reply("And my axe!")
            print("Reply Sent\n")
        except:
            print("Failed to reply to comment\n")
            continue
        replied_ids.appendleft(comment["id"])
        replied_comments.append(comment)

    logChoices(replied_comments, replied_ids)
    return

def checkReplied(reddit,comment):
    com = reddit.comment(id=comment)
    com.refresh()
    if com.replies:
        for comment_replies in com.replies:
            print(comment_replies.body)
            if "axe" in  comment_replies.body:
                return True
            else:
                continue
    return False

def logChoices(comments, ids):
    with open('comment_log.json', 'a') as log:
        for comment in comments:
            entry={
                "author":comment["author"],
                "body":comment["body"],
                "id":comment["id"],
                "subreddit":comment["subreddit"],
                "score":comment["score"]
            }
            json.dump(entry, log, indent=2)
        log.close()

    with open('replied_ids.txt', 'w') as replied:
        for line in ids:
            replied.write(line)
            replied.write("\n")
        replied.close()
    return

if __name__ == "__main__":
    main()
