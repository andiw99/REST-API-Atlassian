from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests

BASE_URL = "https://marketplace.atlassian.com"
ADDONS_URL = f"{BASE_URL}/rest/2/addons"         # Marketplace url stays constant

@api_view(['GET'])      # only get requests
def get_apps(request):
    headers = {
        'Accept': 'application/json',
    }

    params = dict(request.GET)

    try:
        # Make the request to Atlassian Marketplace
        response = requests.get(ADDONS_URL, headers=headers, params=params, timeout=10)
        
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Atlassian Response already contains much information, but we need some special 
            # info like the number of users, which we can obtain through the 'Get app metrics' endpoint of Atlassian        
            # But we also need the vendor, so we use the 'Get app' endpoint, which provides more info
            data = response.json()      # TODO convert to dict ?
            
            apps = []

            for app in data['_embedded']['addons']:         # Atlassian specific, should strictly speaking be handled by an extra class                                
                app_key = app['key']                
                app_response = requests.get(f"{ADDONS_URL}/{app_key}", headers=headers)       # same headers
                app_data = app_response.json()

                # construct a dict with the relevant information
                app_info = {
                    'name': app['name'],
                    'description': app['summary'],
                    'marketplace_href': f"{BASE_URL}{app['_links']['alternate']['href']}",
                    'categories': [category['name'] for category in app['_embedded']['categories']],
                    'vendor': app_data['_embedded']['vendor']['name'],
                    'average_stars': app_data['_embedded']['reviews']['averageStars'],
                    'number_reviews': app_data['_embedded']['reviews']['count'],
                    'number_downloads': app_data['_embedded']['distribution']['downloads'],
                    'number_installs': app_data['_embedded']['distribution']['totalInstalls'],
                    'number_users': app_data['_embedded']['distribution']['totalUsers'],
                }
                apps.append(app_info)
            
            return Response({'addons': apps})
        else:
            return Response(f"Error: {response.status_code}", status=response.status_code)

    except requests.exceptions.Timeout:
        return Response("Request timed out", status=504)
    except requests.exceptions.RequestException as e:
        return Response(f"Request failed: {e}", status=500)