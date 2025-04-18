import logging
import time
from utils.config import Config
from utils.rabbitmq_utils import wait_for_rabbitmq
from models.scheduler import scheduler
from api.agent_events import listen_for_agent_events

logger = logging.getLogger("AzureInteractionsProcessor")

def main():
    wait_for_rabbitmq(Config.RABBITMQ_HOST, Config.RABBITMQ_PORT)
    logger.info("Starting multi-tenant preprocessor service")

    scheduler.start()
    listen_for_agent_events()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Service stopped gracefully")

if __name__ == "__main__":
    main()