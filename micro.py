import pika

# Устанавливаем соединение с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем очереди
channel.queue_declare(queue='hello')
channel.queue_declare(queue='response')

print(' [*] Waiting for messages. To exit press CTRL+C')

# Определяем callback-функцию для обработки сообщений
def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    response_message = body
    
    # Отправляем ответ в очередь "response"
    channel.basic_publish(exchange='',
                          routing_key='response',
                          body=response_message)
    print(f" [x] Sent response: {response_message}")

# Подписываемся на очередь и указываем callback-функцию
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

# Запускаем обработку сообщений
channel.start_consuming()