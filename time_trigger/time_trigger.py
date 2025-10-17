import os
import logging
import datetime
import azure.functions as func
# from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusSubQueue


bp = func.Blueprint()

# SERVICE_BUS_CONNECTION_STR = os.environ["AzureServiceBusConnection"]
# TOPIC_NAME = "mytopic"
# SUBSCRIPTION_NAME = "nysub"

# @bp.timer_trigger(
#     arg_name="mytimer",
#     schedule="0 */1 * * * *",  # Every minute
# )
# def topic_dlq_resend_timer(mytimer: func.TimerRequest):
#     utc_now = datetime.datetime.utcnow().isoformat()
#     logging.info(f"[{utc_now}] Timer trigger fired for Topic DLQ processing.")

#     servicebus_client = ServiceBusClient.from_connection_string(
#         SERVICE_BUS_CONNECTION_STR,
#         logging_enable=True
#     )
    
#     with servicebus_client:
#         # Receiver for DLQ in the subscription
#         dlq_receiver = servicebus_client.get_subscription_receiver(
#             topic_name=TOPIC_NAME,
#             subscription_name=SUBSCRIPTION_NAME,
#             sub_queue=ServiceBusSubQueue.DEAD_LETTER  # This is the DLQ
#         )

#         with dlq_receiver:
#             dlq_messages = dlq_receiver.receive_messages(
#                 max_message_count=10,
#                 max_wait_time=5
#             )

#             if not dlq_messages:
#                 logging.info("No messages found in DLQ.")
#                 return

#             logging.info(f"Found {len(dlq_messages)} message(s) in DLQ.")

#             sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
#             with sender:
#                 for msg in dlq_messages:
#                     try:
#                         body_str = str(msg)
#                         logging.info(f"Resending DLQ message: {body_str}")

#                         # Progress failed data then mark as completed
#                         # new_msg = ServiceBusMessage(body_str)
#                         # sender.send_messages(new_msg)

#                         # Remove message from DLQ
#                         dlq_receiver.complete_message(msg)
                    
#                     except Exception as e:
#                         logging.error(f"Error resending DLQ message: {e}")
#                         dlq_receiver.abandon_message(msg)

#     logging.info("Topic DLQ resend process finished.")

class MaxTryReached(Exception):
    pass


@bp.timer_trigger(schedule="*/1 * * * * *", arg_name="mytimer", use_monitor=False)
@bp.retry(strategy="exponential_backoff", max_retry_count="3",
           minimum_interval="00:00:01",
           maximum_interval="00:01:00")
def timerfunc(mytimer: func.TimerRequest, context: func.Context) -> None:
    logging.info(f'Current retry count: {context.retry_context.retry_count}')
    try:
        if context.retry_context.retry_count == \
                context.retry_context.max_retry_count:
            logging.info(
                f"Max retries of {context.retry_context.max_retry_count} for "
                f"function {context.function_name} has been reached")
            raise MaxTryReached("Max retries has been reached")
        else:
            raise Exception("This is a retryable exception")
    except MaxTryReached as e:
        logging.error(str(e))
    