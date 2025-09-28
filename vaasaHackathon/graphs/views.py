from django.shortcuts import render
import grafana_api
import pandas as pd

from .llm import load_items_from_csv, map_items_to_idemat


# Create your views here.

def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    context = []
    if request.method == 'POST' and request.FILES.get('csv_file'):
        uploaded_file = request.FILES["csv_file"]
        csv_items = load_items_from_csv(uploaded_file)
        result = map_items_to_idemat(csv_items["Issue"].tolist(), topn=20)
        # Read file contents

        result_listed = [progress['matched_process'] for progress in result]
        df_result = pd.DataFrame({"Issue": csv_items["Issue"],
                                  "Categories": result_listed,
                                  "Quantity": csv_items["Quantity"]})
        print(df_result)
    return render(request, 'index.html')

def api_upload_csv(request):
    # API endpoint for CSV upload
    pass

def api_get_data(request):
    # API endpoint to get data
    pass
