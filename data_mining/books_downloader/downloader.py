import os
import time
import requests
import re
import progressbar
from datetime import datetime


class BooksDownloader:
    """
    Класс для сбора текстов книг с сайта большой бесплатной библиотеки http://tululu.org
    Ожидаемый размер библиотеки на диске ~ 30 Gb
    """

    BOOK_MAX_ID = 100000  # ID последней доступной книги

    @staticmethod
    def download_all(destination_path):
        """
        Метод загрузки всех книг формата *.txt из свободной библиотеки.
        :param destination_path: путь для загрузки книг.
        :return: None
        """
        if not os.path.exists(destination_path):
            print('Creating text data path')
            os.makedirs(destination_path)

        print('Books downloading has been started at %s' % datetime.now().ctime())
        for book_id in progressbar.progressbar(range(BooksDownloader.BOOK_MAX_ID), redirect_stdout=True):
            r = requests.get('http://tululu.org/txt.php?id=%d' % book_id, stream=True, allow_redirects=False)
            if r.status_code == 200:
                filename = re.findall(r'filename="?(.+\.txt)"?', r.headers['content-disposition'])[0]
                print('%s with book_id = %d ... downloaded' % (filename, book_id,))
                with open(os.path.join(destination_path, filename), 'wb') as file:
                    for chunk in r.iter_content(1024):
                        file.write(chunk)
            time.sleep(0.1)

        print('Books downloading has been ended at %s' % datetime.now().ctime())
