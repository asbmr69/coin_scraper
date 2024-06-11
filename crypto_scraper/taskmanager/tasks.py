from celery import shared_task
from .models import Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(task_id):
    task = Task.objects.get(id=task_id)
    scraper = CoinMarketCap()
    task.result = scraper.scrape_coin_data(task.coin)
    task.status = 'COMPLETED'
    task.save()
