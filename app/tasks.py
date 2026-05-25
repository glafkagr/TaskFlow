from celery import Celery


from app.celery_worker import celery
celery = Celery('tasks', broker='redis://redis:6379/0')

# @celery.task(name='send_task_reminder')
# def send_task_reminder(user_email, task_title, due_date):
#     from flask_mail import Message
#     from app.extensions import mail
#     msg = Message(
#         subject=f'Task Reminder: {task_title}',
#         recipients=[user_email],
#         body=f"Reminder: {task_title} is due on {due_date}"
#     )
#     mail.send(msg)
#     return f"Email sent to {user_email}"

@celery.task(name='send_task_reminder')
def send_task_reminder(user_email, task_title, due_date):
    print(f"REMINDER: {task_title} due on {due_date} to {user_email}")
    return f"Sent to {user_email}"

@celery.task(name='send_daily_summary')
def send_daily_summary(user_id):
    from flask_mail import Message
    from app.extensions import mail
    from app.models.user import User
    user = User.query.get(user_id)
    if not user:
        return f"User {user_id} not found"
    msg = Message(
        subject='Daily Summary',
        recipients=[user.email],
        body=f"Hello {user.username}, this is your daily summary."
    )
    mail.send(msg)
    return f"Summary sent to {user.email}"


@celery.task
def test_task():
    return "Hello"
