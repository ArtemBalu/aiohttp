import asyncio

import aiohttp


async def main():
    client = aiohttp.ClientSession()

    # Создание пользователя
    response = await client.post(
        "http://127.0.0.1:8080/users",
        json={"name": "James", "password": "TGFet5354%", "email": "jamespeterson@example.com"},
    )
    print(response.status)
    print(await response.json())

    # Запрос существующего пользователя
    response = await client.get(
        "http://127.0.0.1:8080/users/1",
    )
    print(response.status)
    print(await response.json())

    # Запрос несуществующего пользователя
    response = await client.get(
        "http://127.0.0.1:8080/users/100",
    )
    print(response.status)
    print(await response.json())

    # Обновление данных пользователя
    response = await client.patch(
        "http://127.0.0.1:8080/users/1",
        json={"name": "John"},
    )
    print(response.status)
    print(await response.json())

    # Удаление существующего пользователя
    response = await client.delete(
        "http://127.0.0.1:8080/users/1",
    )
    print(response.status)
    print(await response.json())

    # Удаление несуществующего пользователя
    response = await client.get(
        "http://127.0.0.1:8080/users/1546",
    )
    print(response.status)
    print(await response.json())

    # Создание нового пользователя для проверки методов для объявлений
    response = await client.post(
        "http://127.0.0.1:8080/users",
        json={"name": "Andrew", "password": "TGFet55464168%", "email": "andrewbrown@example.com"},
    )
    print(response.status)
    print(await response.json())

    # Создание объявления для Andrew
    response = await client.post(
        "http://127.0.0.1:8080/notes",
        json={"header": "Mitsubishi", "description": "2015, 3000 miles, manual transmition", "owner_id": 2},
    )
    print(response.status)
    print(await response.json())

    # Обновление объявления
    response = await client.patch(
        "http://127.0.0.1:8080/notes/1",
        json={"header": "Mitsubishi Outlander"},
    )
    print(response.status)
    print(await response.json())

    # Запрос существующего объявления
    response = await client.get(
        "http://127.0.0.1:8080/notes/1",
    )
    print(response.status)
    print(await response.json())

    # Запрос несуществующего объявления
    response = await client.get(
        "http://127.0.0.1:8080/notes/100",
    )
    print(response.status)
    print(await response.json())

    # Удаление существующего объявления
    response = await client.delete(
        "http://127.0.0.1:8080/notes/1",
    )
    print(response.status)
    print(await response.json())

    # Запрос удаленного объявления
    response = await client.get(
        "http://127.0.0.1:8080/notes/1",
    )
    print(response.status)
    print(await response.json())

    # Удаление несуществующего объявления
    response = await client.delete(
        "http://127.0.0.1:8080/notes/1546",
    )
    print(response.status)
    print(await response.json())

    await client.close()


asyncio.run(main())