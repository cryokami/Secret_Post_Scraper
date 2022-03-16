import uvicorn
import fastapi
import dbcode

app=fastapi.FastAPI()

@app.get("/langs")
def langs_in_db():
    langs=dbcode.list_available_langs()
    return langs
@app.get("/dbstatus")
def dbstatus():
    stat=dbcode.tables_and_rowcounts()
    return stat
@app.get("/randomsecret")
def randsecret(lang:str):
    tint=dbcode.randrow(lang)
    val=dbcode.secret_by_id(tint,lang)
    return val
@app.get("/secret_id")
def secret_by_id(sec_id,lang="it"):
    try:
        val = dbcode.secret_by_id(sec_id,lang)
        return val
    except Exception:
        return f"id {sec_id} does not exist in table {lang}"


def main():
    # uvicorn.run(app, port=8080, host="0.0.0.0")
    uvicorn.run(app, host="0.0.0.0", port=80)

if __name__ =="__main__":
    main()

