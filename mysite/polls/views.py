import json
import os
from dotenv import load_dotenv
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from checkprice import get_price, get_full_time

load_dotenv()
apiURL = os.getenv("API_URL")

# Create your views here.


def index(request):
    data = get_price(apiURL, get_full_time())
    response = JsonResponse(data)
    return response
