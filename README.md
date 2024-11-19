# API-Gateway

Запускаем RabbitMQ через: docker-compose up -d
А после чего запускаем API Gateway через: uvicorn gateway:app --reload
И просто запускаем через консоль заглушки микросервисов (send - для тестов, cart, order, menu, auth - для работы), которые отвечают обратно этим же сообщением.
Можем проверять отправлять запросы через POSTMAN.
Можно запустить test.py вместо постмена, это проверит работоспособность gateway, rabbitmq и send.
