import aiohttp
import asyncio
import sys
import datetime




async def fetch_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def get_exchange_rates(days):
    today = datetime.date.today()
    exchange_rates = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(days):
            date = today - datetime.timedelta(days=i)
            formatted_date = date.strftime("%d.%m.%Y")
            task = asyncio.ensure_future(fetch_exchange_rates(formatted_date))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for i, data in enumerate(results):
            exchange_rates.append({data['date']: {
                'EUR': {
                    'sale': None,
                    'purchase': None
                },
                'USD': {
                    'sale': None,
                    'purchase': None
                }
            }})

            exchange_rate_list = data.get('exchangeRate', [])

            for rate in exchange_rate_list:
                currency = rate.get('currency')
                if currency == 'EUR':
                    exchange_rates[i][data['date']]['EUR']['sale'] = rate.get('saleRate')
                    exchange_rates[i][data['date']]['EUR']['purchase'] = rate.get('purchaseRate')
                elif currency == 'USD':
                    exchange_rates[i][data['date']]['USD']['sale'] = rate.get('saleRate')
                    exchange_rates[i][data['date']]['USD']['purchase'] = rate.get('purchaseRate')

        return exchange_rates

async def main():
    days = int(sys.argv[1])
    exchange_rates = await get_exchange_rates(days)
    print(exchange_rates)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
