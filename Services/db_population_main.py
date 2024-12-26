import asyncio, aiohttp



async def main():
    async with aiohttp.ClientSession() as session: 
        conn_str=input("Unesite connection string za bazu: ")
        PATH = input("Unesite lokaciju CSV datoteke: ")
        relation_nr = int(input("Unesite broj relacija: "))
        relations = [{"name": input(f"Naziv relacije {i+1}: "), "atributes":input(f"Atributi relacije {i+1}: ").split(","),
                "fk": input(f"Relacija stranog kljuca relacije {i+1}(ako nema nemojet unijeti nista) : " ) or None,
                "uk": input(f"Unique key u relaciji stranog kljuca {i+1}(ako nema nemojet unijeti nista) : " ).split(",")} for i in range(relation_nr)]
        data={"conn_str":conn_str, "path":PATH, "relations":relations}

        population_rez=await session.post("http://localhost:8080/db_population", json=data)
        print(await population_rez.text())

asyncio.run(main())