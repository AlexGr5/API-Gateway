# API-Gateway

1) Запускаем RabbitMQ через: docker-compose up -d

2) А после чего запускаем API Gateway через: uvicorn gateway:app --reload

3) И просто запускаем через консоль заглушки микросервисов (micro - для тестов, cart, order, menu, auth - для работы), которые отвечают обратно этим же сообщением.

4) Можем проверять отправлять запросы через POSTMAN.

5) Можно запустить test.py вместо постмена, это проверит работоспособность gateway, rabbitmq и micro.

Весть проект:
https://docs.google.com/document/d/1wTd1yBbGNlQqCBXM-Z2ftYkNtxiSp5PELhL2fGo2318/edit?usp=sharing
