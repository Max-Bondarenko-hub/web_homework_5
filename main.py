import aiohttp
import asyncio
import platform
import sys
from datetime import datetime, timedelta
from pprint import pprint


async def get_ex_rates(ex_date, ticker_list=["EUR", "USD"]):
    rates_dict = {}
    curr_dict = {}
    final_dict = {}
    uppered_list = []
    rates_link = "https://api.privatbank.ua/p24api/exchange_rates?json&date=" + str(ex_date)
    for el in ticker_list:
        if el.isalpha():
            uppered_list.append(el.upper())
    if not uppered_list:
        uppered_list = ["EUR", "USD"]
    async with aiohttp.ClientSession() as session:
        async with session.get(rates_link) as response:
            # print(response.status)
            if 500 > response.status >= 400:
                return 'Client side error, check your request'
            if response.status >= 500:
                return 'Server side error, try later'
            result = await response.json()
            for curr in result["exchangeRate"]:
                for ticker in uppered_list:
                    if curr["currency"] == ticker:
                        rates_dict["sale"] = curr["saleRateNB"]
                        rates_dict["purchase"] = curr["purchaseRateNB"]
                        new = rates_dict.copy()
                        curr_dict[ticker] = new
                        final_dict[ex_date] = curr_dict
            return final_dict


async def main():
    main_list = []
    other_args = []
    todays_date = datetime.now().date()
    days = 1
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
            if days > 10:
                return "Too many days, please enter 10 days or less"
        except ValueError:
            ...
        for el in sys.argv[1:]:
            other_args.append(el)

    for d in range(days):
        temp_rates_date = todays_date - timedelta(days=d)
        str_date = temp_rates_date.strftime(r"%d.%m.%Y")
        if other_args:
            result = get_ex_rates(str_date, other_args)
        else:
            result = get_ex_rates(str_date)
        main_list.append(result)
    return await asyncio.gather(*main_list)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main())
    pprint(result)
