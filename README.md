**Примечание по нотации:**
1) ? - переменная необязательная (например, str? означает, что в переменной может храниться как строка, так и None)
2) requestBody - тело запроса в формате JSON
3) responseBody - тело ответа в формате JSON

**Описание API:**
1) POST /links/shorten - создает и возвращает сокращенную ссылку \
   requestBody: { \
     url: str \
     expiresAt: datetime.datetime? \
     alias: str? \
   } \
   responseBody: { \
     url: str \
   }

3) GET /links/{short_url} - возвращает полную ссылку на основе короткой ссылки
   responseBody: {
     url: str
   }
  
4) GET /links/{short_url} - возвращает статистику короткой ссылки
   responseBody {
     originalUrl: str
     visits: int
     lastTimeUsed: datetime.datetime
     createdAt: datetime.datetime
   }

5) DELETE /links/{short_url} - удаляет короткую ссылку и возвращает длинную ссылку
   responseBody {
    url: str
   }

6) PUT /links/{short_url} - обновляет короткую ссылку (заменяет длинную) и возвращает новую длинную ссылку
   requestBody: {
     url: str
   }
   responseBody: {
     url: str
   }
   
**Инструкция по запуску:**
1) Запустите run.sh в папке infra, чтобы создать контейнеры с PostgreSQL и Redis
2) Создайте таблицу urls и Sequence seq

**Примеры запросов:**
https://disk.yandex.ru/d/a7QNBneDm7uObQ
