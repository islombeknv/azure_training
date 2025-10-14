import logging

import azure.functions as func

bp = func.Blueprint()

@bp.service_bus_topic_trigger(arg_name="message",
                               topic_name="mytopic",
                               connection="AzureServiceBusConnection",
                               subscription_name="nysub")
def servicebus_topic_trigger(message: func.ServiceBusMessage):
    logging.info("Python ServiceBus topic trigger processed message.")

    if "POISON" in message_body:
        logging.error("Poison message detected in topic!")
        raise Exception("Simulated processing failure")

    message_body = message.get_body().decode("utf-8")
    logging.info("Message Body: " + message_body)