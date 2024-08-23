# attendance/tasks.py
from celery import shared_task
import time

@shared_task
def make_attendance_task(params):
    # Simulate a long-running task
    time.sleep(60)  # Replace with actual task logic
    return "Attendance process completed!"
