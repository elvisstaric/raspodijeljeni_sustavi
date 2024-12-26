import aiohttp, asyncio

async def main():
    async with aiohttp.ClientSession() as session: 
        url=input("Unesite adresu stranice koju zelite testirati: ")
        clients = int(input("Unesite broj klijenata za simulaciju: "))
        test_duration = int(input("Unesite trajanje testa: "))
        interval = int(input("Unesite interval ispisa: "))
        params={"url":url, "clients":clients, "test_duration":test_duration, "interval":interval}
        url_rez=await session.post("http://localhost:8081/post_params", json=params)
        print(await url_rez.text())

        

asyncio.run(main())