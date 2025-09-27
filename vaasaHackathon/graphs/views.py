from django.shortcuts import render
import grafana_api

# Create your views here.

def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        uploaded_file = request.FILES["csv_file"]

        # Read file contents
        file_data = uploaded_file.read().decode("utf-8")  # assuming text file
        print(file_data)  # prints to Django console
        # Handle CSV upload here
        pass
    return render(request, 'index.html')

def api_upload_csv(request):
    # API endpoint for CSV upload
    pass

def api_get_data(request):
    # API endpoint to get data
    pass
