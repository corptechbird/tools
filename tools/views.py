from django.shortcuts import render
import numpy as np
import pandas as pd
import json
from django.http import JsonResponse

message = []
csv = ""
data = {}

def analyze(csv_url):
    dataFrame = None
    global csv
    csv = csv_url
    x = []
    try:
        dataFrame = pd.read_csv(csv_url,
                encoding='utf-8')
        global data
        data = dataFrame
        for column in dataFrame:
            y = []
            y.append(column)
            y.append(dataFrame[column].value_counts())
            x.append(y)
        global message
        message = x
    except:
        pass
    finally:
        pass
    return x

def post_export(request):
    global data
    result = {}
    for column in data:
        dic = []
        values = data[column].value_counts().keys().tolist()
        counts = data[column].value_counts().tolist()
        for i, v in enumerate(values):
            local = {}
            local[v] = counts[i]
            dic.append(local)
        result[column] = dic
    return JsonResponse(result, safe=False)
  
def visualizer_index(request):
    text = ""
    csv_url = ""
    if(request.GET.get('csv_url')):
        text = analyze(request.GET.get('csv_url'))
        csv_url = request.GET.get('csv_url')
    else:
        text = None
    context = {'text': text,
    'csv_url': csv_url}
    return render(request, 'tools/visualizer_index.html', context)

def cross_index(request):
    text = ""
    csv_url = ""
    if(request.GET.get('csv_url')):
        text = analyze(request.GET.get('csv_url'))
        csv_url = request.GET.get('csv_url')
    else:
        text = None
    context = {'text': text,
    'csv_url': csv_url}
    return render(request, 'tools/cross_index.html', context)
