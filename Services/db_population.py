import sqlalchemy
import pandas as pd
from aiohttp import web
from fastapi import FastAPI
from pydantic import BaseModel

class Data(BaseModel):
    conn_str: str
    path:str
    relations: list

app=FastAPI()

@app.post('/db_population')
async def post_db_population(data:Data):
    data=data.model_dump()
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
                id = list(range(1,len(unique)+1))
                unique.insert(0, "id", id)
                unique.to_sql(con=mydb, name=rel.get("name"), if_exists='append', index=False)
            else:
                fk_list= []
                for i, row in df.iterrows():
                    table=pd.read_sql(f"""SELECT * from {rel.get("fk")}""", conn)
                    unique_key = df[rel.get("uk")].iloc[i]
                    fk_list.append((table['id'].loc[table[rel.get("uk")[0]]==unique_key.iloc[0]]).iloc[0])

                new_relation = pd.read_csv(PATH, usecols=rel.get("atributes"), delimiter=',')
                unique = new_relation.drop_duplicates()
                id = list(range(1,len(unique)+1))
                unique.insert(0, "id", id)
                unique.insert(1, f"{rel.get("fk")}_id", fk_list)
                unique.to_sql(con=mydb, name=rel.get("name"), if_exists='append', index=False)

        conn.close()
        rez="Populacija baze uspjesna!"
    except Exception as e:
        rez=e
    return {"message":rez}


