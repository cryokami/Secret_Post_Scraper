from __future__ import annotations
import json
import urllib.parse
from models.secrets import Secret
import requests
import dbcode
import webscraper
from loguru import logger


def translate_it(text: str, lang: str) -> str:
    urltext = urllib.parse.quote(text)

    url = "http://translation:5000/translate"
    payload = f"source=it&target={lang}&q={urltext}&api_key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    respo = requests.request("POST", url, data=payload, headers=headers)
    new = json.loads(respo.text)
    translation = new["translatedText"]
    return translation


def translate_missing_secrets_and_save(lang):
    secret_id_list = dbcode.check_if_fully_translated(lang)
    secret_list = dbcode.get_secret_list_by_id_list(secret_id_list)
    if len(secret_list) == 0:
        logger.info(f"all secrets are fully translated")
    else:
        logger.info(f"{len(secret_list)} secrets left to translate. ")
        for secret in secret_list:
            base_text = secret.secret
            secret_id = secret.id
            translated_text = translate_it(base_text, lang)
            cleaned_text = webscraper.clean_strings_for_db(translated_text)
            newsecret = Secret(secret_id, lang, secret.gender, secret.age, cleaned_text)
            dbcode.save_secret_lang(newsecret, lang)
