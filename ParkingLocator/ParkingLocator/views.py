from django.http import HttpResponse
from django.shortcuts import render

import requests
import json

def index(request):
    return render(request, "index.html", {})

def parking(request):
    auth_head = {"Authorization": "Bearer mi5qSSqdhmrNXBjLq5MBMwuqcS0q8aE4u52fwqrG8CkrBjjksgdV8ZblHdh4ThtDqQVFapfOwrCqadcTH4sJIMhQgEcWpc0bK_9ms_rJ1H-xMT1Amp4tmH_PhAg3X3Yx"}
    city = request.GET.get("city", "")
    endpoint = "https://api.yelp.com/v3/businesses/search?categories=Parking&sort_by=rating&location=" + city

    yelp_res = requests.get(endpoint, headers=auth_head)
    if yelp_res.status_code == 404:
        return HttpResponse("<h1>Could not find any parking lots in " + city + "</h1>")

    res_json = json.loads(yelp_res.text)

    for business in res_json["businesses"]:
        business["score"] = round((business["review_count"] * business["rating"]) / (business["review_count"] + 1), 2)

    res_json["businesses"].reverse()

    return render(request, "parking.html", { "businesses": res_json["businesses"] })
