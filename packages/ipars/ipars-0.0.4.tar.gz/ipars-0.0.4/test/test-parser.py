# from ipars import Pars
from module import Pars
from time import sleep
import os
p = Pars()

# for page in range(1, 138):
#     try:
#         url = f'https://animego.la/anime?sort=a.createdAt&direction=desc&type=animes&page={page}'
#         response = p.get_static_page(url, f'./pages/index{page}.html')
#         print('Скачана страница', page)  
#         sleep(4)
#     except UnboundLocalError:
#         pass
# print('\nСКАЧИВАНИЕ СТРАНИЦ ЗАВЕРШЕНО')
films = []

os_dir = os.listdir('./pages/')
for file in os_dir:
    soup = p.returnBs4Object(f'./pages/{file}')
    cards = soup.find_all(class_='col-12')[:-1]
    for cal in cards:
        title = cal.find(class_='media-body').find('a').text
        link = cal.find(class_='media-body').find('a').get('href')
        image = cal.find(class_='anime-list-lazy lazy').get('data-original')
        films.append({
            'title': title,
            'link': link,
            'image': image
        })
    print('Получены данные из файла: ', file)

# import json

# with open('./films.json', 'w', encoding='utf8') as file:
#     json.dump(films, file, ensure_ascii=False, indent=4)
p.dumpJson(films, './films.json')