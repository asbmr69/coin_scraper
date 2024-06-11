from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer
from .tasks import scrape_coin_data
import uuid
from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return HttpResponse("<h1>Welcome to the Crypto Scraper API</h1><p>Use the provided endpoints to start scraping.</p>")

class StartScraping(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
        
        job = Job.objects.create()
        for coin in coins:
            task = Task.objects.create(job=job, coin=coin)
            scrape_coin_data.delay(task.id)
        
        return Response({'job_id': str(job.id)}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'