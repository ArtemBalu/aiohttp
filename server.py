import json

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, User, engine, init_orm, Note

app = web.Application()


def hash_password(password: str):
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_pasword(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app):
    print("Инициализация ORM")
    await init_orm()
    yield
    print("Закрытие подключения к базе")
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_class, message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


async def get_object_by_id(session, object_cls, object_id):
    obj = await session.get(object_cls, object_id)
    if obj is None:
        raise get_error(web.HTTPNotFound, f"Объект с id {object_id} не найден!")
    return obj


async def add_object(session, object_cls, obj):
    try:
        session.add(obj)
        await session.commit()
    except IntegrityError:
        if object_cls == User:
            raise get_error(web.HTTPConflict, f"Пользователь {obj.name} уже существует!")
        else:
            raise get_error(web.HTTPConflict, f"Объявление {obj.header} уже существует!")
    return obj.id


class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    @property
    def session(self):
        return self.request.session

    async def get_user(self):
        user = await get_object_by_id(self.session, User, self.user_id)
        return user

    async def get(self):
        user = await self.get_user()
        return web.json_response(user.dict)

    async def post(self):
        user_data = await self.request.json()
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        await add_object(self.session, User, user)
        return web.json_response({"id": user.id})

    async def patch(self):
        user_data = await self.request.json()
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = await self.get_user()
        for key, value in user_data.items():
            setattr(user, key, value)
        await add_object(self.session, User, user)
        return web.json_response({"id": user.id})

    async def delete(self):
        user = await self.get_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "Удалено"})


class NoteView(web.View):

    @property
    def note_id(self):
        return int(self.request.match_info["note_id"])

    @property
    def session(self):
        return self.request.session

    async def get_note(self):
        note = await get_object_by_id(self.session, Note, self.note_id)
        return note

    async def get(self):
        note = await self.get_note()
        return web.json_response(note.dict)

    async def post(self):
        note_data = await self.request.json()
        note = Note(**note_data)
        await add_object(self.session, Note, note)
        return web.json_response({"id": note.id})

    async def patch(self):
        note_data = await self.request.json()
        note = await self.get_note()
        for key, value in note_data.items():
            setattr(note, key, value)
        await add_object(self.session, Note, note)
        return web.json_response({"id": note.id})

    async def delete(self):
        note = await self.get_note()
        await self.session.delete(note)
        await self.session.commit()
        return web.json_response({"status": "Удалено"})


app.add_routes(
    [
        web.get("/users/{user_id:\d+}", UserView),
        web.patch("/users/{user_id:\d+}", UserView),
        web.delete("/users/{user_id:\d+}", UserView),
        web.post("/users", UserView),

        web.get("/notes/{note_id:\d+}", NoteView),
        web.patch("/notes/{note_id:\d+}", NoteView),
        web.delete("/notes/{note_id:\d+}", NoteView),
        web.post("/notes", NoteView)
    ]
)

web.run_app(app)