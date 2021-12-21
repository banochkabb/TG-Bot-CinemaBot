import logging
import os
from collections import Counter

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlmodel import Session, SQLModel, create_engine, select

from base import Cinema, get_engine
from parser import search, get_json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m %H:%M:%S')

bot = Bot(token=os.environ.get("TG_TOKEN", "1234:faketoken"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def get_welcome(message: types.Message):
    await message.reply(
        text='Привет!'
             'Я CinemaBot и я умею находить информацию про твой фильм или сериал и кидать ссылки, '
             'где ты можешь его посмотреть! Нажми /help чтобы получить помощь или сразу кидай мне название фильма! ')


@dp.message_handler(commands=["help"])
async def get_help(message: types.Message):
    await message.reply(
        text='Отправь мне название фильма или сериала и я покажу тебе краткую информацию о нем и скину ссылку где его '
             'посмотреть! Так же по команде /history я выведу тебе историю поиска, а по команде /stats покажу сколько '
             'раз предлагался тебе каждый фильм!')


@dp.message_handler(commands=["history"])
async def get_history(message: types.Message):
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Cinema.req_name).where(Cinema.user_id == message.from_user.id)
        list_of_requests = session.exec(statement).all()
        out = ", ".join(map(str, list_of_requests))
        await message.reply(text='''Вот все твои запросы:''')
        await bot.send_message(message.chat.id, out)


@dp.message_handler(commands=["stats"])
async def get_stats(message: types.Message):
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Cinema.actual_ru_name).where(Cinema.user_id == message.from_user.id,
                                                        Cinema.actual_ru_name != '')
        list_of_requests = session.exec(statement).all()
        films_counter = Counter(list_of_requests)
        await message.reply(text='''Вот все фильмы которые я тебе предложил и сколько раз:''')
        out = ''
        for film_name, film_counts in films_counter.items():
            out += f'{film_name} : {film_counts}\n'

        await bot.send_message(message.chat.id, out)


@dp.message_handler()
async def get_film(message: types.Message):
    name = message.text
    search_result = search(await get_json(name))
    out = search_result.meta_inf
    image = search_result.image_url
    if image:
        await bot.send_photo(message.from_user.id, image)
    await bot.send_message(message.from_user.id, text=out)
    if search_result.is_found:
        new_request = Cinema(user_id=message.from_user.id, req_name=name, actual_ru_name=search_result.ru_name)
        engine = create_engine("sqlite:///database.db")
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            session.add(new_request)
            session.commit()


if __name__ == '__main__':
    executor.start_polling(dp)
