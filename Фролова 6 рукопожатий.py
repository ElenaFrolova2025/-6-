import requests
from bs4 import BeautifulSoup
import time


def get_wikipedia_links(url, base_url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        for a in soup.select('div.mw-parser-output a[href^="/wiki/"]'):
            href = a.get('href')
            if ":" not in href:
                full_url = base_url + href
                links.add(full_url)

        return links
    except Exception as e:

        return set()


def find_first_path(start_url, target_url, rate_limit):

    visited = set()
    stack = [(start_url, [start_url])]
    requests_made = 0

    while stack:
        current_url, path = stack.pop()

        if current_url == target_url:
                return path


        if len(path) > 5:

            continue


        if current_url not in visited:
            visited.add(current_url)
            links = get_wikipedia_links(current_url, base_url="https://en.wikipedia.org")
            requests_made += 1


            if requests_made >= rate_limit:

                time.sleep(1)
                requests_made = 0


            for link in links:
                if link not in visited:

                    stack.append((link, path + [link]))

    return None


def main(url1, url2, rate_limit):

    print("Поиск пути от url1 к url2")
    path1 = find_first_path(url1, url2, rate_limit)
    if path1:
        print(f"Путь от {url1} к {url2}:")
        print(" -> ".join(path1))


    else:
        print(f"Путь от {url1} к {url2} не найден за 5 шагов.")

    print("Поиск пути от url2 к url1")
    path2 = find_first_path(url2, url1, rate_limit)
    if path2:
        print(f"Путь от {url2} к {url1}:")
        print(" -> ".join(path2))

    else:
        print(f"Путь от {url2} к {url1} не найден за 5 шагов.")


# Входные данные
url1 = "https://en.wikipedia.org/wiki/Irkutsk_Oblast"
url2 = "https://en.wikipedia.org/wiki/Lake_Baikal"
rate_limit = 10


main(url1, url2, rate_limit)