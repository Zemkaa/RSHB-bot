import requests
from bs4 import BeautifulSoup


def get_html(url):
    web_page = requests.get(url)
    return web_page.text


def get_page_data(html):
    present_loans = []
    index = 0
    soup = BeautifulSoup(html, 'lxml')
    loans = soup.find('div', class_='container').find_all('div', class_='row')
    for loan in loans:
        present_loans.append([])
        usl = []
        try:
            title = loan.find('div',
                              class_='elemip col-md-8 col-xm-12').find('div',
                                                                       class_='rtitle').find('a',
                                                                                             class_='linkip').text
        except:
            title = ''
        try:
            url = 'https://www.rshb.ru' + loan.find('div',
                                                    class_='elemip col-md-8 col-xm-12').find('div',
                                                                                             class_='rtitle').find('a').get('href')
        except:
            url = ''
        try:
            terms = loan.find('div',
                              class_='elemip col-md-8 col-xm-12').find_all('div', class_='col-md-4 col-xs-4 col-sm-4')
            for item in terms:
                usl.append(item.find('span', class_='stavka').text)
        except:
            terms = ''
        if title != '' and url != '':
            present_loans[index].append(title)
            present_loans[index].append(url)
            for item in usl:
                present_loans[index].append(item)
        index += 1
    return present_loans


def main():
    url = "https://www.rshb.ru/natural/loans/"
    return get_page_data(get_html(url))
