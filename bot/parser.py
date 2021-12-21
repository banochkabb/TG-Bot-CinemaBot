import json
import os
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Union

import aiohttp
import googlesearch

KINO_TOKEN = os.environ.get('KINO_TOKEN', '1234')


@dataclass
class SearchResult:
    meta_inf: str
    ru_name: Optional[str] = None
    image_url: Optional[str] = None
    is_found: bool = False


async def get_json(name) -> Union[dict, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={0}&page=1'.format(
                        name), headers={'X-API-KEY': KINO_TOKEN}) as resp:
            if resp.status == HTTPStatus.OK:
                result = await resp.text()
            else:
                return 'Прости, такой фильм я не нашел 😓'
    film_info = json.loads(result)
    if film_info['searchFilmsCountResult'] == 0:
        return 'Прости, такой фильм я не нашел 😓'
    film_info = film_info['films'][0]
    return film_info


def search(film_info) -> SearchResult:
    if 'nameRu' not in film_info:
        return SearchResult(meta_inf='Прости, такой фильм я не нашел 😓')
    out = ''
    out += '🔻 ' + film_info['nameRu']
    if 'nameEn' in film_info and film_info['nameRu'] != film_info['nameEn']:
        out += '/' + film_info['nameEn']
    out += '\n'

    out += 'Год: ' + str(film_info['year']) + '\n'
    out += 'Рейтинг: ' + str(film_info['rating']) + '\n'
    out += 'Жанр: ' + film_info['genres'][0]['genre'] + '\n'
    out += 'Описание: ' + film_info['description'] + '\n'
    for q in googlesearch.search(film_info['nameRu'] + ' ' + str(film_info['year']) + ' смотреть онлайн', lang='ru',
                                 num_results=3)[:3]:
        out += '🍿 ' + q + '\n'
    result = SearchResult(meta_inf=out, ru_name=film_info['nameRu'], image_url=film_info.get('posterUrl'), is_found=True)
    return result
