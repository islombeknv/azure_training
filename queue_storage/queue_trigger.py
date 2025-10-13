import azure.functions as func
import logging

bp = func.Blueprint()

@bp.function_name(name="QueueFunc")
@bp.queue_trigger(arg_name="azqueue", queue_name="myqueue",
                               connection="f4b67f_STORAGE") 
def queue_trigger(azqueue: func.QueueMessage):
    message_body = azqueue.get_body().decode("utf-8")
    logging.info(f"Queue Storage message received: {message_body}")
    if "POISON" in message_body:
        logging.error("Poison message detected in Queue Storage!")
        logging.info(f"Function tried to progress message: {azqueue.dequeue_count} times")
        raise Exception("Simulated processing failure")
    
    logging.info("Message processed successfully.")
