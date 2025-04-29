import asyncio
import sys
import signal
import json

class HelloWorld:
    def __init__(self, form_data):
        self.form_data = form_data
        self.running = True

    async def run(self):
        while self.running:
            print(json.dumps(self.form_data))
            await asyncio.sleep(1)

def print_help():
    help_data = {
        "fields": [
            {
                "name": "user name",
                "type": "text"
            },
            {
                "name": "gender",
                "type": "select",
                "options": ["male", "female"]
            }
        ]
    }
    print(json.dumps(help_data))

def signal_handler(signum, frame):
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        sys.exit(0)

    if len(sys.argv) != 2:
        print("Usage: python hello.py <form_data_json>")
        sys.exit(1)

    try:
        form_data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        sys.exit(1)

    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    hello = HelloWorld(form_data)
    asyncio.run(hello.run()) 