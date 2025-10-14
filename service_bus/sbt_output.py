import logging
import azure.functions as func

bp = func.Blueprint()

@bp.function_name(name="ServiceBusSendMessages")
@bp.route(route="put_message", methods=["GET"])
@bp.service_bus_topic_output(arg_name="message",
                              connection="AzureServiceBusConnection",
                              topic_name="mytopic",
                              subscription_name="nysub")
def service_bus_output(req: func.HttpRequest, message: func.Out[str]) -> func.HttpResponse:
    logging.info("HTTP data received")
    input_msg = req.params.get('message')
    message.set(input_msg)
    return 'OK'