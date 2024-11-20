from fastapi import FastAPI, HTTPException
import pika
import time
import json  # Для работы с JSON
import random

app = FastAPI()

# Настраиваем соединение с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем очереди
channel.queue_declare(queue='hello')
channel.queue_declare(queue='response')

channel.queue_declare(queue='cart')
channel.queue_declare(queue='cart_API')

channel.queue_declare(queue='order')
channel.queue_declare(queue='order_API')

channel.queue_declare(queue='menu')
channel.queue_declare(queue='menu_API')

channel.queue_declare(queue='auth')
channel.queue_declare(queue='auth_API')


#==============================================================================
# Отправить данные в очередь и получить ответ из очереди
def send_request_to_querry_and_get_answer(message, querry_send, querry_get, timeoutsec = 20):
    # Отправляем данные в очередь отправления
    channel.basic_publish(exchange='', routing_key=querry_send, body=message)
    print(f" [x] Sent: {message}")

    # Ждем ответа из очереди получения
    response_message = None
    timeout = timeoutsec  # Таймаут ожидания ответа (в секундах)
    start_time = time.time()

    # Убедимся, что потребление новой очереди начинается корректно
    try:
        for method_frame, properties, body in channel.consume(queue=querry_get, inactivity_timeout=1):
            if body:
                response_message = body.decode()
                print(f" [x] Received response: {response_message}")
                channel.basic_ack(method_frame.delivery_tag)  # Подтверждаем получение
                channel.cancel()  # Останавливаем потребление очереди
                return response_message
                break
    
            # Проверяем, не вышли ли за таймаут
            if time.time() - start_time > timeout:
                print(" [ERROR] Timeout while waiting for response.")
                channel.cancel()  # Останавливаем потребление очереди
                raise HTTPException(status_code=504, detail="Response timeout from receiver")
    except Exception as e:
        print(f" [ERROR] Exception during consume: {e}")
        raise HTTPException(status_code=500, detail=str(e))
#==============================================================================




#==============================================================================
# ТЕСТОВЫЕ ФУНКЦИИ ДЛЯ ПРОВЕРКИ РАБОТОСПОСОБНОСТИ
@app.post("/send")
def send_message(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'hello', 'response', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message

@app.get("/send")
def get_message(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'hello', 'response', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message

@app.put("/send")
def update_message(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'hello', 'response', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message

@app.delete("/send")
def delete_message(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'hello', 'response', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message
#==============================================================================




#==============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ API Gateway КОРЗИНА

# Получить активную Корзину
# Входные данные:
'''
    {
         "user_id": user_id
    }

Выходные данные:
    {
        'user_id': user_id,
        'status': 'success',
        'cart':
        {
            'id': id,
            'user_id': user_id,
            'totalPrice': totalPrice,
            'dishes':
            [
            {
                'id': id,
                'name': name,
                'category': category,
                'size': size,
                'price': price,
                'finalPrice': finalPrice,
                'sauce': sauce,
                'products':
                [
                {
                    'id': id,
                    'name': name,
                    'price': price
                },
                …
                ],
                'added_products':
                [
                …
                ],
                'removed_products':
                [
                …
                ]
            },
            …
            ]
        }
    }

или
    {
        'user_id': user_id,
        'status': 'error',
        'error': 'Cart not found'
    }
'''
@app.get("/cart")
def get_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action": "get_cart",
            "sender": "API",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)

    return response_message


# Очистить текущую корзину
# Input:
'''
    {
         "user_id": user_id
    }

Выходные данные:
    {
        'user_id': user_id,
        'status': 'success',
        'cart':
        {
            'id': id,
            'user_id': user_id,
            'totalPrice': totalPrice,
            'dishes':[ ]
        }
    }

Или
    {
        'user_id': user_id,
        'status': 'error',
        'error': 'Cart not found'
    }
'''
@app.delete("/cart")
def clear_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action:": "clear_cart",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)

    return response_message

# Посмотреть Экземпляр Блюда в корзине
# Input:
'''
    {
        "user_id": user_id,
        "dish_id": dish_id
    }
'''
'''
Выходные данные:
    {
        'user_id': user_id,
        'dish_id': dish_id,
        'status': 'success',
        ‘dish’:
        {
            ‘id’: id,
            ‘name’: name,
            ‘category’: category,
            ‘size’: size,
            ‘price’: price,
            ‘finalPrice’: finalPrice,
            ‘sauce’: sauce,
            ‘products’:
            [
                {
                    ‘id’: id,
                    ‘name’: name,
                    ‘price’: price
                },
            …
            ],
            ‘added_products’: […],
            ‘removed_products’: […]
        },
    }

или
    {
        'user_id': user_id,
        'dish_id': dish_id,
        'status': 'error',
        'error': error
    }
'''
@app.get("/cart/dish")
def get_dish_in_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action": "get_dish",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)

    return response_message

# Добавить в корзину
# Входные данные:
''' {
    "user_id": user_id,
    "dish": { JSON блюда }
    }    
'''
'''
Выходные данные:
    {
        'user_id': user_id,
        'status': 'success',
        'dish':
            {
                'id': id,
                …
            }
    }
'''
@app.post("/cart/dish")
def add_dish_in_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action": "add_dish",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")
    
    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)
    
    return response_message

# Обновить Экземпляр Блюда в корзине
# Input:
'''
    {
        "user_id": user_id,
        "dish_id": dish_id,
        "dish": {JSON Блюда}
    }

Выходные данные:
    {
        'user_id': user_id,
        'status': 'success',
        'dish':
        {
            'id': id,
            …
        }
    }

или
    {
        'user_id': user_id,
        'dish_id': dish_id,
        'status': 'error',
        'error': error
    }
'''
@app.put("/cart/dish")
def update_dish_in_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action": "update_dish",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)

    return response_message


# Удалить Экземпляр Блюда в корзине
# Input:
'''
    {
        "user_id": user_id,
        "dish_id": dish_id
    }

Выходные данные:
    {
        'user_id': user_id,
        'dish_id': dish_id,
        'status': status,
        'message': message
    }
'''
@app.delete("/cart/dish")
def remove_dish_in_cart(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {
            "action": "remove_dish",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'cart', 'cart_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    temp = json.loads(response_message)
    response_message = temp.get('data', None)

    return response_message
#==============================================================================




#==============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ API Gateway ЗАКАЗ

# Сделать заказ
# Input:
"""
    {
        'client_id': client_id,
        'rest_id': restaurant_id,
        'comment': 'Комментарий к заказу',
        'delivery_type': delivery_type,
        'delivery_address': 'г. Новосибирск, ул. Ленина, д. 65, кв. 45'
    }

Выходные данные:
    {
        'order':
        {
            'id': order_id,
            'client_id': client_id,
            'rest_id': rest_id,
            'cour_id': 'cour_id',
            'created_at': created_at_timestamp,
            'estim_time': estim_time,
            'status': status,
            'payment_status': payment_status,
            'delivery_type': delivery_type,
            'delivery_address': 'г. Новосибирск, ул. Ленина, д. 65, кв. 45',
            'cart': {…}
        }
    }

Или
    {
        'id': correlation_id,
        'action': 'create_response',
        'status': 'error',
        'error': 'Error description'
    }
"""
@app.post("/order")
def create_order(data: dict):
    try:
        correlation_id = random.randint(10000000, 99999999)
        
        # Формируем данные для отправки
        transformed_data = {
            "id": correlation_id,
            "action": "create",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'order', 'order_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    if 'data' in response_message:
        temp = json.loads(response_message)
        response_message = temp.get('data', None)

    return response_message


# Получить информацию о заказе
# Input:
'''
    {
         'order_id': order_id
    }

Выходные данные:
    {
        'order':
        {
            'id': order_id,
            'client_id': client_id,
            'rest_id': rest_id,
            'cour_id': 'cour_id',
            'created_at': created_at_timestamp,
            'estim_time': estim_time,
            'status': status,
            'payment_status': payment_status,
            'delivery_type': delivery_type,
            'delivery_address': 'г. Новосибирск, ул. Ленина, д. 65, кв. 45',
            'cart': {…}
        }
    }

Или
    {
        'id': correlation_id,
        'action': 'order_response',
        'status': 'error',
        'error': 'Error description'
    }
'''
@app.get("/order/order")
def get_order(data: dict):
    try:
        correlation_id = random.randint(10000000, 99999999)
        
        # Формируем данные для отправки
        transformed_data = {
            "id": correlation_id,
            "action": "get_order",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'order', 'order_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    if 'data' in response_message:
        temp = json.loads(response_message)
        response_message = temp.get('data', None)
    
    return response_message

# Получить статус
# Input:
'''
    {
         'order_id': order_id
    }

Выходные данные:
    {
        'order_id': order_id,
        'status': status,
        'payment_status': payment_status
    }

Или
    {
        'order_id': order_id
    }
'''
@app.get("/order/status")
def get_status(data: dict):
    try:
        correlation_id = random.randint(10000000, 99999999)
        
        # Формируем данные для отправки
        transformed_data = {
            "id": correlation_id,
            "action": "get_status",
            "data": data
        }
        
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'order', 'order_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    # Получаем данные из ответа от микросервиса
    if 'data' in response_message:
        temp = json.loads(response_message)
        response_message = temp.get('data', None)
    
    return response_message
#==============================================================================





#==============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ API Gateway МЕНЮ

# Получить все Категории
# Input:
# Без парамеров
@app.get("/menu")
def get_categories(data: dict):
    try:
        # Формируем данные для отправки
        transformed_data = {}
        # Преобразуем данные в JSON-строку
        message = json.dumps(transformed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'menu', 'menu_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message

# Получить Блюда
# Input:
    '''
        {
             'category_id': category_id
        }
    '''
@app.get("/menu/dishes")
def get_dishes(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'menu', 'menu_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message

# Получить блюдо
# Input:
    '''
        {
             'dish_id': dish_id
        }
    '''
@app.get("/menu/dish")
def get_dish(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'menu', 'menu_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message
#==============================================================================




#==============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ API Gateway АВТОРИЗАЦИЯ

# Авторизация
# Input:
    '''
        {
             'name': name,
             'phone': phone
        }
    '''
@app.post("/auth")
def authorization(data: dict):
    try:
        message = json.dumps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error serializing data: {e}")

    response_message = None
    response_message = send_request_to_querry_and_get_answer(message, 'auth', 'auth_API', 15)

    if not response_message:
        raise HTTPException(status_code=500, detail="Failed to get response from receiver")

    response_message = json.loads(response_message)
    return response_message
#==============================================================================


@app.on_event("shutdown")
def shutdown_event():
    """
    Закрытие соединения с RabbitMQ при завершении работы сервера.
    """
    connection.close()
