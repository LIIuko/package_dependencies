from bs4 import BeautifulSoup
import requests


def get_file_dependencies_part1(name_package):
    '''Ворзвращает ссылку на github этого пакета'''

    PIP_URL = "https://pypi.org/project/"

    page = requests.get(PIP_URL + name_package)
    if page.status_code != 200:
        print("Error")
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")
    links_html = soup.find_all('a')

    for link_html in links_html:
        if link_html.get('href') is not None \
                and "https://github.com/" in link_html.get("href") \
                and name_package.lower() in link_html.get("href") \
                and link_html.get("href")[-len(name_package) - 1:] == name_package + "/":
            return link_html.get("href")
    return None



def get_file_dependencies_part2(link):
    '''Возвращает вторую часть ссылки на файл с зависимостьями'''

    page = requests.get(link)
    if page.status_code != 200:
        print("Error")
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")
    links_html = soup.find_all('a')

    for link_html in links_html:
        if link_html.get('href') is not None and "setup.py" in link_html.get("href"):
            return link_html.get("href")
    return None



def get_file_dependencies(name_package):
    '''Возвращает ссылку на файл с зависимостьями пакета'''

    link_part1 = get_file_dependencies_part1(name_package)
    if link_part1 is None:
        print("Error")
        return

    repeated_part = link_part1.replace("https://github.com/", "")

    link_part2 = get_file_dependencies_part2(link_part1)
    if link_part2 is None:
        print("Error")
        return

    print(link_part1[:-1] + link_part2.replace(repeated_part, ""))


if __name__ == '__main__':
    package = "flask" #input("Введите название пакета для которого нужно вывести дерево зависимостей: ")
    get_file_dependencies(package)