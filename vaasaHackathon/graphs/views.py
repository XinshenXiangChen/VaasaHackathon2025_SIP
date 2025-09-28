from django.shortcuts import render, redirect
import grafana_api
import pandas as pd
from django.utils import timezone

from .llm import load_items_from_csv, map_items_to_idemat
from .models import Proces, UploadedData  # Add UploadedData import


# Create your views here.

def visualization(request):
    return render(request, 'visualization.html')  # Empty container page for now

def index(request):
    return render(request, 'index.html')

def upload_csv(request):
    context = {}  # Initialize context as empty dict
    if request.method == 'POST' and request.FILES.get('csv_file'):
        uploaded_file = request.FILES["csv_file"]
        csv_items = load_items_from_csv(uploaded_file)
        result = map_items_to_idemat(csv_items["Issue"].tolist(), topn=20)
        # Read file contents
        
        # unit_list =
        # carbon_dioxide_list =
        # total_eco_cost_list =
        # e1_list =
        # e2_list =
        # e3_list =
        # e4_list =
        # e5_list =

        result_listed = [progress['matched_process'] for progress in result]
        
        # Create a mapping from category to unit for each name
        unit_mapping = {}
        
        # Query PostgreSQL for each category to get the corresponding unit
        for i, category in enumerate(result_listed):
            # Get the first matching process for this category
            matching_process = Proces.objects.filter(
                process_name__icontains=category
            ).values('unit', 'carbon_dioxide', 'total_eco_costs', 
                    'eco_costs_e1', 'eco_costs_e2', 'eco_costs_e3', 
                    'eco_costs_e4', 'eco_costs_e5').first()
            
            if matching_process:
                unit_mapping[csv_items["Issue"].iloc[i]] = {
                    'unit': matching_process['unit'],
                    'carbon_dioxide': matching_process['carbon_dioxide'],
                    'total_eco_costs': matching_process['total_eco_costs'],
                    'eco_costs_e1': matching_process['eco_costs_e1'],
                    'eco_costs_e2': matching_process['eco_costs_e2'],
                    'eco_costs_e3': matching_process['eco_costs_e3'],
                    'eco_costs_e4': matching_process['eco_costs_e4'],
                    'eco_costs_e5': matching_process['eco_costs_e5']
                }
                
                # Debug: Print the mapping for each name
                print(f"Name: {csv_items['Issue'].iloc[i]} -> Category: {category} -> Unit: {matching_process['unit']}")
            else:
                print(f"No match found for category: {category}")
                unit_mapping[csv_items["Issue"].iloc[i]] = {
                    'unit': 'Unknown',
                    'carbon_dioxide': 0,
                    'total_eco_costs': 0,
                    'eco_costs_e1': 0,
                    'eco_costs_e2': 0,
                    'eco_costs_e3': 0,
                    'eco_costs_e4': 0,
                    'eco_costs_e5': 0
                }
        
        # Create lists for each attribute based on the mapping
        unit_list = [unit_mapping[name]['unit'] for name in csv_items["Issue"]]
        carbon_dioxide_list = [unit_mapping[name]['carbon_dioxide'] for name in csv_items["Issue"]]
        total_eco_cost_list = [unit_mapping[name]['total_eco_costs'] for name in csv_items["Issue"]]
        e1_list = [unit_mapping[name]['eco_costs_e1'] for name in csv_items["Issue"]]
        e2_list = [unit_mapping[name]['eco_costs_e2'] for name in csv_items["Issue"]]
        e3_list = [unit_mapping[name]['eco_costs_e3'] for name in csv_items["Issue"]]
        e4_list = [unit_mapping[name]['eco_costs_e4'] for name in csv_items["Issue"]]
        e5_list = [unit_mapping[name]['eco_costs_e5'] for name in csv_items["Issue"]]
        
        # Debug: Print the extracted lists
        print("\n=== Extracted Lists Debug ===")
        print(f"Unit list: {unit_list}")
        print(f"Carbon dioxide list: {carbon_dioxide_list}")
        print(f"Total eco cost list: {total_eco_cost_list}")
        print(f"E1 list: {e1_list}")
        print(f"E2 list: {e2_list}")
        print(f"E3 list: {e3_list}")
        print(f"E4 list: {e4_list}")
        print(f"E5 list: {e5_list}")
        
        # Create a new dataframe with the results including all attributes
        df_result = pd.DataFrame({
            "Name": csv_items["Issue"],
            "Category": result_listed,
            "Quantity": csv_items["Quantity"],
            "Unit": unit_list,
            "Carbon_Dioxide": carbon_dioxide_list,
            "Total_Eco_Costs": total_eco_cost_list,
            "Eco_Costs_E1": e1_list,
            "Eco_Costs_E2": e2_list,
            "Eco_Costs_E3": e3_list,
            "Eco_Costs_E4": e4_list,
            "Eco_Costs_E5": e5_list
        })
        print("\n=== CSV Result DataFrame ===")
        print(df_result)
        
        # Save DataFrame to PostgreSQL database
        print("\n=== Clearing existing data ===")
        # Delete all existing records from uploaded_data table
        deleted_count = UploadedData.objects.all().delete()[0]
        print(f"Deleted {deleted_count} existing records from uploaded_data table")
        
        print("\n=== Saving to Database ===")
        saved_count = 0
        for index, row in df_result.iterrows():
            try:
                UploadedData.objects.create(
                    name=row['Name'],
                    category=row['Category'],
                    quantity=row['Quantity'],
                    unit=row['Unit'],
                    carbon_dioxide=row['Carbon_Dioxide'],
                    total_eco_costs=row['Total_Eco_Costs'],
                    eco_costs_e1=row['Eco_Costs_E1'],
                    eco_costs_e2=row['Eco_Costs_E2'],
                    eco_costs_e3=row['Eco_Costs_E3'],
                    eco_costs_e4=row['Eco_Costs_E4'],
                    eco_costs_e5=row['Eco_Costs_E5']
                )
                saved_count += 1
                print(f"Saved: {row['Name']} -> {row['Category']}")
            except Exception as e:
                print(f"Error saving {row['Name']}: {str(e)}")
        
        print(f"\nSuccessfully saved {saved_count} records to database")
        
        # Add the saved data to context for display
        context = {
            'df_result': df_result,
            'saved_count': saved_count,
            'total_records': len(df_result)
        }

    #return render(request, 'index.html', context)
    return redirect('visualization')

def api_upload_csv(request):
    # API endpoint for CSV upload
    pass

def api_get_data(request):
    # API endpoint to get data
    pass
