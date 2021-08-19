from celery.decorators import task
from celery.utils.log import get_task_logger
from .emails import send_confirmation_email

logger = get_task_logger(__name__)
@task(name="send_verification_email_task")
def send_verification_email_task(user):
    logger.info("confirmation email Sent")
    return send_confirmation_email(user)