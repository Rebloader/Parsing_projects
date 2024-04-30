import requests
from lxml import html
import pandas as pd


# url = 'https://worldathletics.org/records/by-category/world-records'


def page_scrapper(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    })
    try:
        tree = html.fromstring(response.content)
        rows = tree.xpath('//*[@id="men"]/table/tbody/tr')
        result_list = []
        for row in rows:
            row_data = row.xpath('.//td/text()')

            record = {}
            record['DISCIPLINE'] = row.xpath(".//td[1]/a/text()")[0].strip()
            record['Progression'] = 'up' if row_data[1] else '0'
            record['PERF'] = row_data[4].strip()
            record['WIND'] = float(row_data[5].strip() if row_data[5].strip() else "0")
            record['Competitor'] = row.xpath(".//td[5]/a/text()")[0].strip() \
                if row.xpath(".//td[5]/a/text()") \
                else row_data[6].strip()
            record['DOB'] = row_data[8].strip() if row_data[8].strip() else "0"
            record['COUNTRY'] = row_data[10].strip() if len(row_data[10].strip()) == 3 else row_data[9].strip()
            record['VENUE'] = row_data[11].strip() if len(row_data[11].strip()) != 11 else row_data[10].strip()
            record['DATE'] = row_data[11].strip() if len(row_data[11].strip()) == 11 else row_data[12].strip()
            print(record)

            result_list.append(record)
        return result_list
    except Exception as e:
        print(e)
        return []


def save_to_csv(result_list):
    df = pd.DataFrame(result_list)
    df.to_csv('file_result.csv')


def main():
    result = page_scrapper('https://worldathletics.org/records/by-category/world-records')
    save_to_csv(result)
    return result


if __name__ == '__main__':
    main()

