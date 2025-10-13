import azure.functions as func
import logging

bp = func.Blueprint()

@bp.function_name(name="QueuePoisonFunc")
@bp.queue_trigger(arg_name="azqueue", queue_name="myqueue-poison",
                               connection="f4b67f_STORAGE") 
def queue_poison_trigger(azqueue: func.QueueMessage):
    message_body = azqueue.get_body().decode("utf-8")
    logging.info(f"poisoned message received: {message_body}")