# Тестовое задание

## Инструкция
Для начала нужно клонировать данный репозиторий

```
git clone https://github.com/FancyDogge/testovoe_quizes.git
```

Вас уже будет ждать готовый docker-compose.yml и приложение flask с Dockerfile

Убедитесь, что вы находитесь в директории с docker-compose.yml и введите следующую команду для сборки образа:

```
docker-compose build
```

Должна начаться сборка образа, в процессе которой, благодаря Dockerfile в приложении flask, установятся все необходимые для него зависимости

Далее, чтобы создать контейнеры и в следствии запустить приложение с сервером, введите

```
docker-compose up

если хотите, чтобы процесс запустился в бэкграунде:

docker-compose up -d
```

Все готово!
Теперь приложение запущено на порте 5000 вашей локальной машины и принимает post запрос по адресу 127.0.0.1:5000/get_quiz

Пример запроса:

сохранит в дб 10 вопросов и вернет предыдущий сохраненный вопрос, если таковой имеется
```
POST /get_quiz HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Content-Length: 21

{"questions_num": 10}
```

Пример запроса с помощью python requests

На респонс можно посмотреть с помощью print(response.json())

```
import requests
response = requests.post('http://127.0.0.1:5000/get_quiz',
                    json={"questions_num": 10}
                    )
print(response.json())
```

