from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests

MP_URL = "https://marketplace.atlassian.com/rest/2/addons"         # Marketplace url stays constant

@api_view(['GET'])      # only get requests
def get_apps(request):
    headers = {
        'Accept': 'application/json',
    }

    params = dict(request.GET)
    print(params)

    try:
        # Make the request to Atlassian Marketplace
        response = requests.get(MP_URL, headers=headers, params=params, timeout=10)
        
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response if needed
            data = response.json()
            print(data)
            return JsonResponse(data)  # Return the JSON response as an API response
        else:
            return Response(f"Error: {response.status_code}", status=response.status_code)

    except requests.exceptions.Timeout:
        return Response("Request timed out", status=504)
    except requests.exceptions.RequestException as e:
        return Response(f"Request failed: {e}", status=500)