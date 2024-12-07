import sqlalchemy
import pandas as pd
from aiohttp import web
from aiohttp.web import AppRunner
import asyncio, aiohttp


async def post_db_population(req):
    data=await req.json()
    conn_str=data.get("conn_str")
    
    PATH = data.get("path")
    df = pd.read_csv(PATH, delimiter=",") 
    relations = data.get("relations")

    try:
        mydb = sqlalchemy.create_engine(conn_str)
        conn=mydb.connect()
        for rel in relations:
            if rel.get("fk") is None:
                new_relation = pd.read_csv(PATH, usecols=rel.get("atributes"), delimiter=',')
                unique = new_relation.drop_duplicates()
                """ values={atr:unique[atr] for atr in rel.get("atributes")}
                df_values = pd.DataFrame({'name':values.keys(), 'value':values.values()})"""
                id = list(range(1,len(unique)+1))
                unique.insert(0, "id", id)
                print(unique)
                unique.to_sql(con=mydb, name=rel.get("name"), if_exists='append', index=False)
        conn.close()
        rez="Populacija baze uspjesna!"
    except Exception as e:
        rez=e
    return web.json_response(rez)
app = web.Application()
app.router.add_post('/db_population', post_db_population)

async def start_server():
    runner = AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Poslužitelj sluša na http://localhost:8080")

async def main():
    await start_server() 
    async with aiohttp.ClientSession() as session: 

        conn_str=input("Unesite connection string za bazu: ")
        PATH = input("Unesite lokaciju CSV datoteke: ")
        relation_nr = int(input("Unesite broj relacija: "))
        relations = [{"name": input(f"Naziv relacije {i+1}: "), "atributes":input(f"Atributi relacije {i+1}: ").split(","),
                "fk": input(f"Strani kljuc relacije {i+1}(ako nema nemojet unijeti nista) : " ) or None} for i in range(relation_nr)]
        data={"conn_str":conn_str, "path":PATH, "relations":relations}

        population_rez=await session.post("http://localhost:8080/db_population", json=data)
        print(await population_rez.text())
asyncio.run(main()) 

