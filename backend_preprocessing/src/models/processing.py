import json
import csv
import io
import redis
import pika
from utils.azure_storage import read_azure_file, write_azure_file
from utils.config import Config
from utils.data_transforms import group_flat_messages, transform_log, create_interactions
from models.agent import fetch_agent_config

def process_data(agent_id: str):
    print(f"Starting data processing for {agent_id}")

    agent_config = fetch_agent_config(agent_id)
    if not agent_config:
        print(f"ERROR: Configuration not found for {agent_id}")
        return

    log_path = "amazonq_conversations.json"
    map_path = "amazonq_json_mapping.json"
    output_file = "amazon_interactions.json"

    try:
        log_content = read_azure_file(log_path)
        mapping_content = read_azure_file(map_path)
        if log_path.endswith(".json"):
            log_data = json.loads(log_content)
        elif log_path.endswith(".csv"):
            log_data = list(csv.DictReader(io.StringIO(log_content)))
        else:
            raise ValueError("Unsupported file format")

        mapping_data = json.loads(mapping_content)

        if isinstance(log_data, list) and log_data and "role" in log_data[0]:
            transformed_data = group_flat_messages(log_data, mapping_data)
        else:
            transformed_data = transform_log(log_data, mapping_data)

        interactions = create_interactions(transformed_data)
        write_azure_file(output_file, json.dumps(interactions))

        # Redis integration
        redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)
        agent_queue_key = f"interactions_queue:{agent_id}"
        for interaction in interactions:
            redis_client.lpush(agent_queue_key, json.dumps(interaction))

        # RabbitMQ notification
        try:
            credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                credentials=credentials,
                heartbeat=60
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            message_body = json.dumps({'agent_id': agent_id})
            print(f"DEBUG: Attempting to send message: {message_body}")
            channel.basic_publish(
                exchange='',
                routing_key='message_queue',
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    expiration='600000'
                )
            )
            print(f"✅ Sent ready message for {agent_id}")
        except Exception as e:
            print(f"ERROR: ❌ Failed to send ready message: {e}")
        finally:
            try:
                connection.close()
            except Exception as close_err:
                print(f"ERROR: ❌ Error closing connection: {close_err}")

        print(f"Processed {len(interactions)} interactions for {agent_id}")

    except Exception as e:
        print(f"ERROR: Processing failed for {agent_id}: {e}")