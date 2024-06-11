from django.urls import path
from .views import StartScraping, ScrapingStatus

urlpatterns = [
    path('start_scraping/', StartScraping.as_view(), name='start_scraping'),
    path('scraping_status/<uuid:id>/', ScrapingStatus.as_view(), name='scraping_status'),
]