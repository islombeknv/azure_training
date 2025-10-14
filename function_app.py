import azure.functions as func 
from queue_storage import queue_trigger, queue_output, queue_poison_trigger
from service_bus import sbq_trigger, sbt_trigger, sbt_output
from time_trigger import time_trigger

app = func.FunctionApp() 

blueprints = [
    queue_poison_trigger.bp,
    queue_output.bp,
    queue_trigger.bp,
    sbq_trigger.bp,
    sbt_trigger.bp,
    sbt_output.bp,
    time_trigger.bp
    
]

for bp in blueprints:
    app.register_functions(bp)