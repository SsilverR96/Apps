from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup as BS
import re


def index(request):
    return render(request, 'main/index.html')


@csrf_exempt
def content(request):
    domain = ''
    if request.method == 'POST':
        domain = request.POST['domain']

    r = requests.get(domain)
    html = BS(r.content, 'html.parser')

    location_data = (str(re.findall('data:\[.+\]', str(html)))).split('},')

    inlocations = []
    for el in location_data:
        if re.search('"parent_location":"".*', str(el)):
            temp = re.sub('"', '', el)
            temp2 = re.sub('.*name:', '', temp)
            inlocations.append(temp2)

    locations = []
    for loc in inlocations:
        temp = re.sub('\\\\\\\\u0107', 'ž', loc)
        temp2 = re.sub('\\\\\\\\u010', 'č', temp)
        temp3 = re.sub('\\\\\\\\u017e', 'ž', temp2)
        temp4 = re.sub('\\\\\\\\u0160', 'Š', temp3)
        temp5 = re.sub('\\\\\\\\u0161', 'š', temp4)
        temp6 = re.sub('\\\\\\\\u017d', 'Ž', temp5)
        locations.append(temp6)

    searchpage = (html.select('#listings_results_form'))[0].get('action')

    transactions = html.select('#listings_results_form #id_transaction option')

    links = []
    meta = {}
    if len(locations) != 0:
        for el in transactions:
            for loc in locations:
                if el.text == 'Za prodaju':
                    meta = {'type': 'sale_strict', 'location_ids': 'Should_be_' + loc + ''}
                elif el.text == 'Za najam':
                    meta = {'type': 'rent_strict', 'location_ids': '"Should_be_' + loc + '"'}
                link = {'url': searchpage + '?id_transaction=' + el.get('value') + '&location=' + re.sub(' ', '+', loc) + '&page=[INDEX]', 'meta': meta}
                links.append(link)
    elif len(transactions) != 0:
        for el in transactions:
            if el.text == 'Za prodaju':
                meta = {'type': 'sale_strict', 'location_ids': 'Should_be_Country'}
            elif el.text == 'Za najam':
                meta = {'type': 'rent_strict', 'location_ids': 'Should_be_Country'}
            link = {'url': searchpage + '?id_transaction=' + el.get('value') + '&page=[INDEX]', 'meta': meta}
            links.append(link)
    else:
        return HttpResponse('Error')

    context = {'urls': links}
    source = {'source': context}
    config = {'config': source}

    return JsonResponse(config)
