from celery import Celery
from . import services
import datetime


app = Celery('converter', broker='redis://localhost:6379')

app.conf.update(
    timezone='UTC',
)


# @app.task(bind=True, max_retries=3, default_retry_delay=60)
# def convert_currency(self, from_currency: str, to_currency: str, amount: float):
#     try:
#         converted_amount, rate = currency_service.get_rate(from_currency, to_currency, amount)
#         return {
#             'message': f'Запрос на конвертацию {amount} {from_currency} в {to_currency} был сделан в {datetime.datetime.now()}.'
#         }
#     except Exception as exc:
#         self.retry(exc=exc)
