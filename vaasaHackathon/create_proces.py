# create_proces.py
import os
import django

# Step 1: Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaasaHackathon.settings")  # Replace myproject with your project name
django.setup()

# Step 2: Import your model
from graphs.models import Proces

# Step 3: Insert a new row
Proces.objects.create(
    lci_number=3,
    unit="m3",
    process_name="Refining",
    carbon_dioxide=300,
    total_eco_costs=800,
    eco_costs_e1=80,
    eco_costs_e2=160,
    eco_costs_e3=120,
    eco_costs_e4=200,
    eco_costs_e5=240
)

print("Process inserted successfully!")

# Optional: Verify by printing all entries
for proces in Proces.objects.all():
    print(proces.lci_number, proces.process_name, proces.total_eco_costs)
