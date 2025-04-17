from tortoise import Tortoise
from models import Task

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    print("init_db()")
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()