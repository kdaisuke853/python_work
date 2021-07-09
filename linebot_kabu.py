from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime, timezone, timedelta
import sys, re
import requests
from bs4 import BeautifulSoup


def price_now_return(company_code):
    site = 'https://www.nikkei.com/nkd/company/?scode={}'.format(company_code)

    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'lxml')

    val = soup.find('dd', attrs={'class': 'm-stockPriceElm_value now'})
    val2 = str(val)

    a1 = re.search(r'[0-9]*(,|[0-9])[0-9]*', val2)

    price_now = a1.group(0)

    price_now = price_now.replace(',', '')
    # price_now = price_now.replace('.', '')
    price_now2 = float(price_now)

    return price_now2


"""
def price_now_return(company_code):
    site = requests.get(
        'https://stocks.finance.yahoo.co.jp/stocks/chart/?code=%s' % company_code)

    data = BeautifulSoup(site.text, 'html.parser')

    # print(data.title)

    price = data.find_all('td', {'class': 'stoksPrice'})
    price_now = price[1].text

    price_now = price_now.replace(',', '')
    # price_now = price_now.replace('.', '')
    price_now2 = float(price_now)

    return price_now2
"""


def price_get_close(company_code):
    company_code = company_code + '.T'
    my_share = share.Share(company_code)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                              2,
                                              share.FREQUENCY_TYPE_MINUTE,
                                              1)

    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    date_2 = symbol_data['timestamp']

    old_date = date_2[0]
    now_date = date_2[len(date_2) - 1]

    old_time = datetime.fromtimestamp(old_date / 1000)
    now_time = datetime.fromtimestamp(now_date / 1000)

    price = symbol_data["close"]
    old_price = price[0]
    now_price = price[len(date_2) - 1]
    # print(datetime.fromtimestamp(date_2[0] / 1000))
    # print(str(old_time) + "の株価:" + str(old_price))
    # print(str(now_time) + "の株価:" + str(now_price))
    old_price = float(old_price)

    return old_price


def judege_notify(word):
    send_line_notify('%s の株価が高いです' % word)


def send_line_notify(notification_message):
    line_notify_token = '8MYwhc4uXBQ9ijZxAJFz2lWwcrz2OLE7cvXiLUlguKs'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers=headers, data=data)

    # judege_notify()
    # kabu_get_price(2, 1, '3902.T')  # 日曜日にやると土日の分になるため値を持ってこれない


data_dict = {7201: '日産自動車',
             7202: 'いすゞ自動車',
             7203: 'トヨタ自動車',
             7205: '日野自動車',
             7211: '三菱自動車工業',
             7261: 'マツダ',
             7267: '本田技研工業',
             7269: 'スズキ',
             7270: 'SUBARU',
             7272: 'ヤマハ発動機',
             6902: 'デンソー'}

# code = '3676.T'
if __name__ == '__main__':
    for mykey, company_name in data_dict.items():
        code = str(mykey)
        a = price_now_return(code)
        b = price_get_close(code)
        if a > b:
            judege_notify(code)
