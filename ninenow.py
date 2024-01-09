import os 
import toml 
import re
import subprocess
import logging
import time 
from pushover import Pushover

po = Pushover(str(os.environ["PUSHOVER_APP"]))
po.user(str(os.environ["PUSHOVER_USER"]))

BASE_DIR = "/mnt/ninenow/"
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

show_dict = toml.load("shows.toml")

# print(shows)
queued_downloads = []

for show in show_dict:
    if not os.path.exists(f"{BASE_DIR}{show}"):
        os.mkdir(f"{BASE_DIR}{show}")
    for season in show_dict[show]:
        if show_dict[show][season]["active"]:
            if not os.path.exists(f"{BASE_DIR}{show}/{season}"):
                os.mkdir(f"{BASE_DIR}{show}/{season}")
            episodes = os.listdir(f"{BASE_DIR}{show}/{season}")
            latest_episode = 0
            max = 0
            for episode in episodes:
                try:
                    max = int(re.findall(r"Episode_(\d+)", episode)[0])
                except:
                    pass
                if max > latest_episode:
                    latest_episode = max
            if latest_episode == 0:
                latest_episode = 1
                if show == "9news-sydney" and season == "season-2024":
                    # TODO: Have a better way of getting the inital news episode. Can't rely on working fowards from episode 1 as it does not exist. 
                    latest_episode = 3
                elif show == "australian-open-tennis" and season == "2019":
                    # TODO:
                    latest_episode = 21
                elif show == "australian-open-tennis" and season == "2022":
                    # TODO:
                    latest_episode = 13
            else:
                # TODO: This feels wrong
                latest_episode +=1
            cmd = (["yt-dlp", "--no-mtime", "--verbose", "--restrict-filenames", "-o", f"{BASE_DIR}{show}/{season}/Episode_{latest_episode}_%(title)s_[%(id)s].%(ext)s", f"https://www.9now.com.au/{show}/{season}/episode-{latest_episode}"]) 
            logging.info(" ".join(cmd))
            try:
                subprocess.check_output(cmd)
                # send pushover notif
                msg = po.msg(f"Latest episode of {show.replace('-', ' ').title()} has been downloaded.")
                msg.set("title", f"9Now Downloader")
                po.send(msg)
            except Exception as e:
                print(str(e))
                # episode doesn't exist - 404? probably should log 
                pass
