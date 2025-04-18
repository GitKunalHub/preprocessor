from models.scheduler import scheduler
from models.agent import fetch_agent_config
from models.processing import process_data
import logging

logger = logging.getLogger("AzureInteractionsProcessor")

def schedule_agent_processing(agent_id: str):
    agent_config = fetch_agent_config(agent_id)
    if not agent_config:
        logger.error(f"Agent {agent_id} configuration not found")
        return

    schedule_config = agent_config.get('scheduling', {})
    job_id = f"agent_{agent_id}"

    # Remove existing job if present
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"Removed existing job for agent {agent_id}")

    try:
        schedule_type = schedule_config.get('type', 'daily')
        start_time = schedule_config.get('start_time', '00:00')

        if schedule_type == 'minutely':
            job = scheduler.add_job(
                process_data,
                'interval',
                minutes=1,
                args=[agent_id],
                id=job_id
            )
        elif schedule_type == 'hourly':
            job = scheduler.add_job(
                process_data,
                'interval',
                hours=1,
                args=[agent_id],
                id=job_id
            )
        elif schedule_type == 'daily':
            hour, minute = map(int, start_time.split(':'))
            job = scheduler.add_job(
                process_data,
                'cron',
                hour=hour,
                minute=minute,
                args=[agent_id],
                id=job_id
            )
        elif schedule_type == 'weekly':
            job = scheduler.add_job(
                process_data,
                'interval',
                weeks=1,
                args=[agent_id],
                id=job_id
            )
        elif schedule_type.endswith('h'):
            job = scheduler.add_job(
                process_data,
                'interval',
                hours=int(schedule_type[:-1]),
                args=[agent_id],
                id=job_id
            )
        else:
            logger.error(f"Unsupported schedule type: {schedule_type}")
            return

        logger.info(f"Scheduled {schedule_type} processing for {agent_id}")
        logger.debug(f"Next run time for agent {agent_id}: {job.next_run_time}")
        process_data(agent_id)  # Immediate first run

    except Exception as e:
        logger.error(f"Scheduling failed for {agent_id}: {e}")