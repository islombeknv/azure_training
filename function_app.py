import azure.functions as func 
from queue_storage import queue_trigger, queue_output, queue_poison_trigger
from service_bus.trigger import bp as bp_svbus

app = func.FunctionApp() 

blueprints = [
    queue_poison_trigger.bp,
    queue_output.bp,
    queue_trigger.bp
]

for bp in blueprints:
    app.register_functions(bp)