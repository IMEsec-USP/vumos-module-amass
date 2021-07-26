import asyncio

from common.messaging.vumos import ScheduledVumosService

loop = asyncio.get_event_loop()


def task(service: ScheduledVumosService, _: None = None):
    print("TODO: Do important things")
    # For sending data, use the built-in service class functions
    # They follow the following format:
    # - send_[type]_data()
    # example:
    service.send_target_data("0.0.0.0", domains=[], extra={
        "extra": "Some extra data!"
    })


# Initialize Vumos service
service = ScheduledVumosService(
    "Scheduled Service Template",
    "Template for a service that runs periodically",
    conditions=lambda s: True, task=task, parameters=[
        {
            "name": "Example Parameter",
            "description": "Just an example",
            "key": "example",
            "value": {
                "type": "string",
                "default": "template"
            }
        }],
    pool_interval=10  # Runs task every 10 seconds
)

loop.run_until_complete(service.connect(loop))
loop.run_until_complete(service.loop())
