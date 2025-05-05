import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get("https://wikipedia.org/")
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/'):
            links.append(href)
    return links

def check_six_handshakes(start_url, end_url):
    visited = set()
    queue = [(start_url, 0)]
    while queue:
        current_url, depth = queue.pop(0)
        if current_url.endswith (current_url):
            return True
        if depth >= 6:
            break
        if current_url not in visited:
            visited.add(current_url)
            links = get_links(current_url)
            for link in links:
                queue.append((link, depth + 1))
    return False

start_url = "https://en.wikipedia.org/wiki/Lake_Baikal"
end_url = "https://en.wikipedia.org/wiki/Irkutsk_Oblast"

result = check_six_handshakes(start_url, end_url)
if result:
    print("Теория шести рукопожатий подтверждается для выбранных статей.")
else:
    print("Теория шести рукопожатий не подтверждается для выбранных статей.")
