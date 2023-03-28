import asyncio
import platform
import argparse
from datetime import datetime, timedelta

from multiprocessing import Process, current_process

import aiohttp

DEFAULT_LIST_CURRENCY = ["EUR", "USD"]
LIMIT = 1


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    print(f"Error status: {resp.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            print(f'Connection error: {url}', str(err))


async def main(res_limit, res_currency):
    p1_ = datetime.today()
    answer = []
    for i in range(res_limit):
        add_new_date_key = (p1_ - timedelta(days=i)).strftime("%d.%m.%Y")
        result = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={add_new_date_key}")
        cur_result = result.get("exchangeRate")
        if result:
            dict_parse = {}
            for cur in res_currency:
                try:
                    exc, = list(filter(lambda el: el["currency"] == cur, cur_result))
                    dict_cur = {
                        cur:
                            {'sale': (exc.get('saleRate') if exc.get('saleRate') else 'немає даних'),
                             'purchase': (exc.get('purchaseRate') if exc.get('purchaseRate') else 'немає даних')}}
                except ValueError as err:
                    dict_cur = {cur: f'error: {err}'}
                dict_parse = dict_parse | dict_cur
                new_dict_parse = {add_new_date_key: dict_parse}
            answer.append(new_dict_parse)
    return answer


def pars_result_for_chat():
    pass


def start_from_message(message):
    pars_message = message.strip().split()
    print(pars_message)

    # for

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)


    return pars_message


def conditions(argums: dict):
    print(argums)
    try:
        res_limit = int(argums.get("limit"))
        if res_limit >= 10:
            res_limit = 10
        elif res_limit <= 1:
            res_limit = 1
            # print(res_limit, type(res_limit))
    except ValueError as err:
        print(f"error: {err}")
        res_limit = LIMIT

    c1 = argums.get("currency")
    res_currency = DEFAULT_LIST_CURRENCY
    if bool(c1):
        res_currency.append(c1)

    return res_limit, res_currency


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Currency Privat Bank")
    print(f"{parser.description} \nfor example: >>> py pars_message.py -l 2 -c GBP")
    parser.add_argument("--limit", "-l", default="1", help="Limit day - no more than the last 10 days")
    parser.add_argument("--currency", "-c", default="", help="Currency")
    args = vars(parser.parse_args())
    # print(type(args))

    limit, currency = conditions(args)

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(limit, currency))

    # - to chat
    print(r)
