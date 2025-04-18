import json
import pika
import time
import logging
from utils.config import Config
from models.schedule_manager import schedule_agent_processing
from models.scheduler import scheduler

logger = logging.getLogger("AzureInteractionsProcessor")

def listen_for_agent_events():
    credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=Config.RABBITMQ_HOST,
        credentials=credentials
    )

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            def callback(ch, method, properties, body):
                try:
                    event = json.loads(body)
                    event_message = event.get('message')
                    agent_id = event.get('agent_id')

                    if event_message == 'AgentCreated':
                        logger.info(f"Processing AgentCreated for {agent_id}")
                        schedule_agent_processing(agent_id)
                    elif event_message == 'delete':
                        job_id = f"agent_{agent_id}"
                        if scheduler.get_job(job_id):
                            scheduler.remove_job(job_id)
                            logger.info(f"Removed job for {agent_id}")
                    else:
                        logger.info(f"Ignoring event with message: {event_message}")

                except Exception as e:
                    logger.error(f"Error processing message: {e}")

            channel.basic_consume(
                queue='agent_events',
                on_message_callback=callback,
                auto_ack=True
            )
            logger.info("Listening for agent events...")
            channel.start_consuming()

        except Exception as e:
            logger.error(f"RabbitMQ connection error: {e}, retrying in 5s...")
            time.sleep(5)