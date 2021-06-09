from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import JsonResponse
from .predict import *

# Create your views here.
@api_view(['GET'])
def predict(request):
  dataset, train, prediction = getPrediction()

  return JsonResponse({
    "dataset": json.dumps(dataset.tolist()), 
    "train": json.dumps(train.tolist()), 
    "prediction": json.dumps(prediction.tolist())
  })

