# Библиотека для работы с файлами во время парсинга

Во время работы часто приходится скачивать html страницы, работать с json файлами. Эта библиотека призвана облегчить написание кода для такого рода задач.

Установить библиотеку:
```bash
pip install ipars
```

## Пример кода
```python
# Импортируем библиотеку
from ipars import Pars
# Создаём объект класса
p = Pars()
```

## Коротко о методах
1. Функция **get_static_page** принимает url страницы, путь по которому сохранится страница, метод записи и заголовки запроса. Метод записи "wb" используется для сохранения кортинок, по умолчанию writeMethod установлен как "w", что используется для html-страниц. Если заголовки запросов не указаны, то будут использоваться встроенные, но при желании можно указать свои. Функция возвращает статус ответа сайта, что должно использоваться для введения проверок
```python
from ipars import Pars
p = Pars()
# Заголовки для запроса
headers ={
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
    }
# Делаем запрос к сайту и записываем статус ответа в переменную
status_response = p.get_static_page('https://google.com', './index.html', headers=headers)
if status_response == 404:
    print('Страница не найдена')
```

2. Функция **get_dinamic_page** с помощью библиотеки Selenium получает динамически обновляемую страницу. Это помогает когда контент на странице подгружается динамически. Принимает url страницы, путь сохранения и closeWindow. По умолчанию браузер Selenium открывается в фоновом режиме и работу браузара не видно, но если closeWindow указать как False, то будет видень процес выполнения кода

3. Функция **returnBs4Object** возвращает объект beautifulsoup4. Принимает путь до html страницы, содержимое которой преобразует в объект beautifulsoup, кодировку открытия файла (по умолчанию UTF-8) и тип парсера (по умолчанию lxml)
```py
from ipars import Pars
p = Pars()
p.get_static_page('https://google.com', './index.html')
# Получаем объект beautifulsoup из полученной страницы
soup = p.returnBs4Object('./index.html')
# Используем методы beautifulsoup
allImage = soup.find_all('img')
```

4. Метод **loadJson** используется для получения данных из json файла по указанному пути. 

5. Метод **dumpJson** используется для записи данных в json файл. Принимает данные для записи и путь до файла

```py
from ipars import Pars
p = Pars()
# Записываем данные
p.dumpJson([1,2,3,4,5,6,7], './data.json')
# Получаем данные
data = p.loadJson('./data.json') # [1,2,3,4,5,6,7]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
