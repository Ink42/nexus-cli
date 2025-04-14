import redis
import yaml
import threading

# Load Configuration from YAML File
def load_config(yaml_file):
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Load Configuration
config = load_config('config.yaml')

# Connect to Redis
r = redis.Redis(host=config['redis']['host'],
                port=config['redis']['port'],
                db=config['redis']['db'])

# Define the channel name (from the config file)
channel_name = config['redis']['channel_name']

# Produce Message (using the channel from the config)
def produce_message(message):
    r.publish(channel_name, message)

# Consume Message (with proper PubSub handling)
def consume_message(channel, callback):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    print(f"Subscribed to channel: {channel}")
    for message in pubsub.listen():
        if message['type'] == 'message':
            callback(channel, message['data'].decode())

# Example Callback function:
def callback(channel, message):
    print(f"Received message on channel {channel}: {message}")
    # Perform the next step (e.g., run tests)
    print("Running tests...")

# Start the consumer in a separate thread
consumer_thread = threading.Thread(target=consume_message, args=(channel_name, callback))
consumer_thread.daemon = True
consumer_thread.start()

# Simulate a build completing
produce_message("Build complete successfully!")
