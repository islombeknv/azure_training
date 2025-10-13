import azure.functions as func 
from queue_storage_trigger import bp as bp_queue
from servicebus_trigger import bp as bp_svbus

app = func.FunctionApp() 

app.register_functions(bp_queue)