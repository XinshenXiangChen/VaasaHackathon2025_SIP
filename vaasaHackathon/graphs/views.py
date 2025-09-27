from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        # Handle CSV upload here
        pass
    return render(request, 'graphs/index.html')

def api_upload_csv(request):
    # API endpoint for CSV upload
    pass

def api_get_data(request):
    # API endpoint to get data
    pass
