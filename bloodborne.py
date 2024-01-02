import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from colorama import Fore
from pprint import pprint

@dataclass
class Item:
    name: str
    url: str

def welcome(categories):
    """ Welcome User """

    for index, category in enumerate(categories):
        index += 1
        print(Fore.LIGHTBLACK_EX + f'{index} -- {category}')

    user_select = int(input('Enter Category: '))

    return user_select

def collect_categories_list(url):
    """ Collecting categories: only {Characters, Bosses, Locations} """

    response = httpx.get(url)
    html = HTMLParser(response.text)

    main_div = html.css_first('div.mw-parser-output').css_first('tr')

    categories_tag = main_div.css('a')
    categories = []
    for category in categories_tag:
        categories.append(category.attributes['title'])

    return categories

def parse_category(category):
    """ Parsing Category """

    url = f'https://bloodborne.fandom.com/wiki/{category}'
    response = httpx.get(url)
    html = HTMLParser(response.text)
    domen = 'https://bloodborne.fandom.com/'

    names_and_urls_tag = html.css('a.category-page__member-link')

    names = []
    urls = []
    for info in names_and_urls_tag:

        # names
        names.append(info.attrs['title'])

        # urls
        urls.append(domen + info.attrs['href'])

    for i in range(len(names)):
        item = Item(
            name=names[i],
            url=urls[i]
        )

        pprint(item)

    return '\nDone !!!'

def main():
    """ MAIN func """

    try:
        url = 'https://bloodborne.fandom.com/wiki/Bloodborne_Wiki'
        categories = collect_categories_list(url)
        user_input = welcome(categories)

        print(parse_category(categories[user_input - 1]))

    except Exception:
        print(Fore.RED + '\nWrong input. Type number of category correctly !!!')

if __name__ == '__main__':
    main()

