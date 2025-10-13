import azure.functions as func
import logging

bp = func.Blueprint()

@bp.function_name(name="QueueOutput")
@bp.route(route="message/send", methods=["post"])
@bp.queue_output(arg_name="msg", 
                  queue_name="myqueue", 
                  connection="f4b67f_STORAGE")
def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    input_msg = req.get_json()
    
    logging.info(input_msg)

    msg.set(input_msg)

    logging.info("Message sent to outputqueue")
    return func.HttpResponse("Message queued!")