import os
from typing import List

import yaml

LOGGERS = "\x54\x68\x65\x43\x68\x61\x6D\x70\x75\x42\x6F\x74"  # connect errors api key "Dont change it"

languages = {}
languages_present = {}


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except:
        print("ᴛʜᴇʀᴇ ɪs sᴏᴍᴇ ɪssᴜᴇ ᴡɪᴛʜ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ғɪʟᴇ ɪɴsɪᴅᴇ ʙᴏᴛ.")
        exit()
