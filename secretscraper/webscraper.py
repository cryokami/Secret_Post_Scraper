from __future__ import annotations
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from loguru import logger
import os

import translation
from models.secrets import Secret
import dbcode

global ACCEPTED_LANGS
ACCEPTED_LANGS = (
    "en",
    "ar",
    "zh",
    "nl",
    "fi",
    "fr",
    "de",
    "hi",
    "hu",
    "id",
    "ga",
    "ja",
    "ko",
    "pl",
    "pt",
    "ru",
    "es",
    "sv",
    "tr",
    "uk",
    "vi",
)




def clean_strings_for_db(text: str) -> str:
    newtext = text.replace('''"''', """``""").replace("'", """`""")
    return newtext


def get_secret_it(pages):
    options = Options()
    options.add_argument("--headless")
    genders = (
        "male",
        "female",
        "other",
    )  # iterating through genders to avoid advertisements which would otherwise lead to errors.
    secrets = []
    with webdriver.Firefox(options=options) as driver:
        for page_num in range(1, pages + 1):
            url = f"https://insegreto.com/it?page={page_num}"
            driver.get(url)
            for gender in genders:
                secret_list = driver.find_elements(
                    By.XPATH, f'//article[@data-gender="{gender}"]'
                )
                for secret in secret_list:
                    secret_gender = secret.get_attribute("data-gender")
                    secret_id = secret.get_attribute("data-id")
                    secret_lang = "it"
                    message_element = secret.find_element(
                        By.CLASS_NAME, "secret__message"
                    )
                    secret_text = clean_strings_for_db(message_element.text)
                    agestr = secret.find_element(By.CLASS_NAME, "secret__title").text
                    age = int(
                        "".join(filter(str.isdigit, agestr))
                    )  # Age extracted from the title via filter
                    secrets.append(
                        Secret(secret_id, secret_lang, secret_gender, age, secret_text)
                    )
    logger.info(f"found {len(secrets)} entries")
    return secrets


def start():
    pagestr: int = os.getenv("PAGES")  # uses the env vars set in the docker compose.
    langs: str = os.getenv("LANGS_CS")
    try:
        pages = int(pagestr)
    except:
        logger.info(f"could not translate {pagestr} into an integer, defaulting to 5")
        pages = 5

    lowelangs = langs.lower()
    language_list: list = lowelangs.split(",")
    print(language_list)
    logger.info(language_list)
    dbcode.create_secrets_db_it()
    dbcode.save_secret_it(get_secret_it(pages))

    for lang in language_list:
        if lang in ACCEPTED_LANGS:
            dbcode.create_table_for_language(lang)
            translation.translate_missing_secrets_and_save(lang)
            logger.info(f"finished translating {lang}")
        else:
            logger.info(
                f"{lang} is not in the list of accepted languages. "
            )


def main():
    start()


if __name__ == "__main__":
    main()
