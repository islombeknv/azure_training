import logging
import azure.functions as func

bp = func.Blueprint()

@bp.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="myservicebusqueue",
    connection="ServiceBusConnection"
)
def servicebus_trigger(msg: func.ServiceBusMessage):
    message_body = msg.get_body().decode("utf-8")
    logging.info(f"Service Bus message received: {message_body}")

    if "POISON" in message_body:
        logging.error("Poison message detected in Service Bus!")
        # Failing enough times will push to DLQ automatically
        raise Exception("Simulated failure for Service Bus message")
    
    logging.info("Message processed successfully.")