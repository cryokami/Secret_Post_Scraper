from __future__ import annotations

import psycopg2
import sqlalchemy.engine
from sqlalchemy.exc import IntegrityError
from models.secrets import Secret
from loguru import logger
import collections

sqcr = sqlalchemy.engine.cursor.LegacyCursorResult
dblink = sqlalchemy.engine.create_engine(
    "postgresql+psycopg2://aaron:postgres@database:5432/secrets"
)

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
    "it",
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


def send_query_string(query: str):
    with dblink.connect() as con:
        res = con.execute(query)
        return res


def create_secrets_db_it():
    query = "create table if not exists secrets_it (ID int not null,sedex serial,  gender text not null, age smallint not null, secret text not null, primary key(ID));"
    # sedex to enable easy sampling of random rows
    send_query_string(query)
    logger.info("created initial db and table for italian")


def create_table_for_language(language: str):
    if language not in ACCEPTED_LANGS:
        logger.info(f"code {language} not found in supported languages. skipping")
        return
    else:
        query = f"create table if not exists secrets_{language} (ID int not null, secret text not null, primary key(id), constraint fk_sec_id foreign key(ID) references secrets_it(ID));"
        res = send_query_string(query)
        logger.info(f"created table for{language} ")
        return res


def save_secret_it(secrets: list):
    for secret in secrets:
        secret_text = secret.secret
        secret_gender = secret.gender
        secret_id = secret.id
        secret_age = secret.age
        query = f"insert into secrets_it(id,gender,age,secret) values ('{secret_id}','{secret_gender}','{secret_age}','{secret_text}');"
        try:
            send_query_string(query)
        except:
            logger.info(f"secret with id{secret_id} already exists")


def save_secret_lang(secret: Secret, lang):
    query = f"insert into secrets_{lang}(id,secret) values('{secret.id}','{secret.secret}');"
    try:
        send_query_string(query)
    except IntegrityError:
        logger.info("exists")


def sqlalchemy_tuple_to_list(sqtuple) -> list:
    listofill = []
    for value in sqtuple:
        listofill.append(value[0])
    return listofill


def check_if_fully_translated(lang) -> bool:
    query1 = "select id from secrets_it "
    res1 = send_query_string(query1)
    query2 = f"select id from secrets_{lang}"
    res2 = send_query_string(query2)
    list1 = sqlalchemy_tuple_to_list(res1.all())
    list2 = sqlalchemy_tuple_to_list(res2.all())
    difference_list = list(set(list1) - set(list2))
    return difference_list


def get_secret_list_by_id_list(idlist: list):
    secret_list = []
    for number in idlist:
        query = f"select * from secrets_it where id={number}"
        res: sqcr = send_query_string(query)
        for result in res.all():
            secidid, sedex, gender, age, text = result
            secret_list.append(Secret(secidid, "it", gender, age, text))
    return secret_list


if __name__ == "__main__":
    pass
