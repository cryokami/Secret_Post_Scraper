from __future__ import annotations
import random
import psycopg2
import sqlalchemy.engine

dblink = sqlalchemy.engine.create_engine(
    "postgresql+psycopg2://aaron:postgres@database:5432/secrets"
)
sqrs=sqlalchemy.engine.LegacyCursorResult
def execute_query(query:str):
    with dblink.connect() as con:
        res=con.execute(query)
        return res
def get_row_count_lang(lang):
    query=f"select count(*) from secrets_{lang}"
    res:sqrs=execute_query(query)
    return res.one()[0]

def list_available_langs():
    query="select * from pg_catalog.pg_tables where schemaname !='information_schema' and schemaname!='pg_catalog';"
    res=execute_query(query)
    langlist=[]
    for result in res.all():
        langlist.append(result[1][8:])
    return langlist
def sqlalchemy_tuple_to_list(sqtuple) -> list:
    listofill = []
    for value in sqtuple:
        listofill.append(value[0])
    return listofill
def tables_and_rowcounts():
    langlist=list_available_langs()
    retstring=""
    for lang in langlist:
        rc=get_row_count_lang(lang)
        retstring=retstring+f"secrets_{lang} contains {rc} rows, "
    return retstring
def randrow(lang):
    query=f"select id from secrets_{lang};"
    res=execute_query(query)
    ls=sqlalchemy_tuple_to_list(res.all())
    sl=random.sample(ls,1)
    return sl[0]


def secret_by_id(secid, lang:str="it"):
    if lang.lower()=="it":
        query = f"select * from secrets_{lang} where id={secid};"
        res = execute_query(query)
        secid, sedex, gender, age, secret = res.all()[0]
        return [secid, gender, age, secret]
    else:
        query1=f"select * from secrets_it where id={secid}"
        res=execute_query(query1)
        secid,sedex,gender,age,secret=res.all()[0]
        query2=f"select * from secrets_{lang} where id={secid}"
        res2=execute_query(query2)
        secid,secret=res2.all()[0]
        return [secid ,gender, age, secret]


