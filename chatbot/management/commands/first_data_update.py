from django.core.management.base import BaseCommand
from chatbot.updater import data_update

class Command(BaseCommand):
    help = 'My custom command to run a Python file'

    def handle(self, *args, **options):
        # Add your Python file execution code here
        try:
            print(data_update.payer_transitions_data(self))
            print(data_update.imaging_studies_data(self))
            print(data_update.immunization_data(self))
            print(data_update.careplan_data(self))
            print(data_update.condition_data(self))
            print(data_update.organizations_data(self))
            print(data_update.encounter_data(self))
            print(data_update.devices_data(self))
            print(data_update.patients_data(self))
            # data_update.allergies_data(self)
        except Exception as e:
            print(f'Data update failed: {str(e)}')
        print("Data updated successfully")