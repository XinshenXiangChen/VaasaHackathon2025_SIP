import pandas as pd
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaasaHackathon.settings")  # Replace myproject with your project name
django.setup()


# Path to your local Excel file
file_path = "C:/Users/anoua/OneDrive/Escritorio/Hackathons/Junction/idemat2025_db.xlsx"

# Read the first sheet

ds = pd.read_excel(file_path, usecols = "C,E,F,G,H,I,J,K,L,M", header=None)
ds = ds.drop(1)
ds = ds.drop(2)
ds = ds.dropna()

print(ds.iloc[0,0])

from graphs.models import Proces


for i,row in enumerate(ds.itertuples(index = False)):
    Proces.objects.create(
        lci_number=str(ds.iloc[i,0]),
        unit=str(ds.iloc[i,1]),
        process_name=str(ds.iloc[i,2]),
        carbon_dioxide=ds.iloc[i,3],
        total_eco_costs=ds.iloc[i,4],
        eco_costs_e1=ds.iloc[i,5],
        eco_costs_e2=ds.iloc[i,6],
        eco_costs_e3=ds.iloc[i,7],
        eco_costs_e4=ds.iloc[i,8],
        eco_costs_e5=ds.iloc[i,9],
    )

for proces in Proces.objects.all():
    print(proces.lci_number, proces.process_name, proces.total_eco_costs)

