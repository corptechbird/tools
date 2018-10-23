from django.shortcuts import render
import numpy as np
import pandas as pd
import json
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv

message = []
csv = ""
data = {}

def localanalyze(csv_url):
    dataFrame = None
    global csv
    csv = csv_url
    x = []
    # try:
    csv_url = "http://techbird.site:8080/static/tools/media/" + csv_url
    dataFrame = pd.read_csv(csv_url, error_bad_lines=False, encoding='utf-8')
    print(dataFrame)
    global data
    data = dataFrame
    for column in dataFrame:
        y = []
        y.append(column)
        y.append(dataFrame[column].value_counts())
        x.append(y)
    global message
    message = x
    # except:
    #     pass
    # finally:
    #     pass
    return x

def remoteanalyze(csv_url):
    dataFrame = None
    global csv
    csv = csv_url
    x = []
    try:
        dataFrame = pd.read_csv(csv_url, encoding='utf-8')
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

def cross(csv_url):
    dataFrame = None
    global csv
    csv = csv_url
    x = []
    try:
        dataFrame = pd.read_csv(csv_url,
                encoding='utf-8')
        global data
        data = dataFrame
        df = pd.crosstab(dataFrame['sex'], dataFrame['pclass'])
        idx = pd.IndexSlice
        x.append(df.values.tolist())
            #     print(c)
        #     for local in dataFrame:
        #         if column != local:
        #             y = []
                    # y.append(column)
                    # y.append(local)
                    # df = pd.crosstab(dataFrame[column], dataFrame[local])
                    # isCalculated = false
                    # for index, rows in df.iterrows():
                    #     if isCalculated == false:
                    #         columns = []
                    #         for row in rows:
                    #             columns.append(row)
                    #         y.append(columns)
                    #     print(index)
                    #     print(rows)
                    # x.append(df)
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
        text = remoteanalyze(request.GET.get('csv_url'))
        csv_url = request.GET.get('csv_url')
    else:
        text = None
    context = {'text': text,
    'csv_url': csv_url}
    
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        text = localanalyze(filename)
        fs.delete(myfile.name)
        return render(request, 'tools/visualizer_index.html', {
            'text': text
        })

    return render(request, 'tools/visualizer_index.html', context)

def cross_index(request):
    text = ""
    csv_url = ""
    if(request.GET.get('csv_url')):
        text = cross(request.GET.get('csv_url'))
        csv_url = request.GET.get('csv_url')
    else:
        text = None
    context = {'text': text,
    'csv_url': csv_url}
    return render(request, 'tools/cross_index.html', context)

def pivot_index(request):
    text = ""
    csv_url = ""
    if(request.GET.get('csv_url')):
        text = analyze(request.GET.get('csv_url'))
        csv_url = request.GET.get('csv_url')
    else:
        text = None
    context = {'text': text,
    'csv_url': csv_url}
    return render(request, 'tools/pivot_index.html', context)