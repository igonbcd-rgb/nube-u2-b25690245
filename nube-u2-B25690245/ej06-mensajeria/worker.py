import json, time, pika

def procesar(canal, metodo, props, cuerpo):
    msg = json.loads(cuerpo)
    time.sleep(1) # simula la inferencia del modelo
    print("predicción lista para", msg["id"])
    canal.basic_ack(delivery_tag=metodo.delivery_tag) # confirmar AL FINAL
    
conexion = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
canal = conexion.channel()
canal.queue_declare(queue="inferencias", durable=True)
canal.basic_qos(prefetch_count=1) # un mensaje a la vez por worker
canal.basic_consume(queue="inferencias", on_message_callback=procesar)
print("esperando mensajes...")
canal.start_consuming()