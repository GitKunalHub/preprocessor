from models.scheduler import scheduler
from models.agent import fetch_agent_config
from models.processing import process_data

def schedule_agent_processing(agent_id: str):
    agent_config = fetch_agent_config(agent_id)
    print(f"DEBUG: Agent configuration for {agent_id}: {agent_config}")
    if not agent_config:
        print(f"ERROR: Agent {agent_id} configuration not found")
        return

    schedule_config = agent_config.get('scheduling', {})
    job_id = f"agent_{agent_id}"

    # Remove existing job if present
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        print(f"Removed existing job for agent {agent_id}")

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
            print(f"ERROR: Unsupported schedule type: {schedule_type}")
            return

        print(f"Scheduled {schedule_type} processing for {agent_id}")
        print(f"DEBUG: Next run time for agent {agent_id}: {job.next_run_time}")
        process_data(agent_id)  # Immediate first run

    except Exception as e:
        print(f"ERROR: Scheduling failed for {agent_id}: {e}")