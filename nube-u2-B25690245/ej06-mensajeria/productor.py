import json, uuid, pika

conexion = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
canal = conexion.channel()
canal.queue_declare(queue="inferencias", durable=True) # sobrevive reinicios

for producto in [12, 15, 21]:
    msg = {"id": str(uuid.uuid4()), "producto_id": producto,"mes": 11, "precio": 99.0}
    canal.basic_publish(
       exchange="", routing_key="inferencias", body=json.dumps(msg),
       properties=pika.BasicProperties(delivery_mode=2)) # persistente
    print("enviado", msg["id"])
conexion.close()