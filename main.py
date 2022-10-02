from bs4 import BeautifulSoup
import requests


def get_file_dependencies_part1(name_package):
    """Ворзвращает ссылку на github этого пакета"""

    PIP_URL = "https://pypi.org/project/"

    page = requests.get(PIP_URL + name_package)
    if page.status_code != 200:
        # print("Error in part 1")
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")
    links_html = soup.find_all('a')

    for link_html in links_html:
        if link_html.get('href') is not None \
                and "https://github.com/" in link_html.get("href") \
                and name_package.lower() in link_html.get("href") \
                and (link_html.get("href")[-len(name_package) - 1:] == name_package + "/"
                     or link_html.get("href")[-len(name_package):] == name_package):
            return link_html.get("href")
    return None


def get_file_dependencies_part2(link):
    """Возвращает вторую часть ссылки на файл с зависимостьями"""

    page = requests.get(link)
    if page.status_code != 200:
        # print("Error in part 2")
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")
    links_html = soup.find_all('a')

    for link_html in links_html:
        if link_html.get('href') is not None and "setup.py" in link_html.get("href"):
            return link_html.get("href")
    return None


def get_file_dependencies(name_package):
    """Возвращает ссылку на файл с зависимостьями пакета"""

    link_part1 = get_file_dependencies_part1(name_package)
    if link_part1 is None:
        # print("Link 1 is none")
        return None

    repeated_part = link_part1.replace("https://github.com/", "")

    link_part2 = get_file_dependencies_part2(link_part1)
    if link_part2 is None:
        # print("Link 2 is none")
        return None

    # print(link_part1[:-1] + link_part2.replace(repeated_part, ""))
    return link_part1 + link_part2.replace(repeated_part, "")[1:]


def get_name_packages(page_url):
    """Возвращает названия зависимых пакетов"""
    # print(page_url)
    page = requests.get(page_url)
    if page.status_code != 200:
        # print("Error")
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")

    name_packages = []

    flag = False
    body_fail = soup.find_all('tr')
    for line in body_fail:
        if "]" in line.text:
            flag = False
        if flag:
            first_index = line.text.find('"') + 1
            last_index = line.text[first_index:].find(" ") + first_index
            last_index = line.text[first_index:].find(">") + first_index if line.text[first_index:].find(" ") == -1 else last_index
            name_packages.append(line.text[first_index:last_index].replace(";", ""))
        if "install_requires=[" in line.text \
                or "install_requires = [" in line.text \
                or "requires = [" in line.text:
            flag = True
    return name_packages


def work(package, tab):
    url = get_file_dependencies(package)
    if url is not None:
        if get_name_packages(url) is not None:
            for name in get_name_packages(url):
                if name is None:
                    continue
                print("\t" * tab + package + " -> " + name)
                work(name, tab + 1)


if __name__ == '__main__':
    package = input("Введите название пакета для которого нужно вывести дерево зависимостей: ")
    print(package)
    work(package, 0)