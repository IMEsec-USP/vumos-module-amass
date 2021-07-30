import asyncio
from sys import stdout
from common.messaging.vumos.vumos import VumosServiceStatus
import shlex
import json

from common.messaging.vumos import ScheduledVumosService

loop = asyncio.get_event_loop()


async def task(service: ScheduledVumosService, _: None = None):
    print("Performing scan...")
    # Get domains
    domains: str = service.get_config("domains")
    domains = domains.split(',')
    domains = list(map(lambda d: d.strip(), domains))

    for domain in domains:
        # Set status
        print(f"Scanning domain {domain}")
        service.set_status(VumosServiceStatus(
            "running", f"scanning domain {domain}"))

        # Perform scan, sending json output to stdout
        amass = await asyncio.subprocess.create_subprocess_shell(f"amass enum -nolocaldb -noalts -d {shlex.quote(domain)} -json /dev/stdout",
                                                                 stdout=asyncio.subprocess.PIPE)

        # Parse stdout while subprocess is running
        while True:
            data = await amass.stdout.readline()
            if len(data) == 0:
                break

            line = data.decode('utf-8').rstrip()

            # If it is a json parseable line
            try:
                data = json.loads(line)

                for address in data["addresses"]:
                    ip = address["ip"]

                    # Ignore anything other than ipv4 addresses
                    if len(ip.split(".")) != 4:
                        continue

                    await service.send_target_data(ip, [data["name"]], {
                        data["name"]: {
                            "amass-tag": data["tag"],
                            "amass-sources": data["sources"]
                        }
                    })

            except:
                pass

        await amass.wait()

    print("Finished scan")


# Initialize Vumos service
service = ScheduledVumosService(
    "Periodic Amass Scanner",
    "A amass scanners that performs extensive DNS enumerations on a list of domains periodically",
    conditions=lambda s: True, task=task, parameters=[
        {
            "name": "Domains",
            "description": "List of domains to perform enumerations on",
            "key": "domains",
            "value": {
                "type": "string",
                "default": "seijihariki.top"  # "default.local"
            }
        }],
    pool_interval=60 * 60 * 24  # Runs task every day
)

loop.run_until_complete(service.connect(loop))
service.loop(loop)
