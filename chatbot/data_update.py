import time
import logging
from django.core.management.base import BaseCommand
from chatbot.updater import data_update


class Command(BaseCommand):
    help = 'Updates data every 12 hours'

    def handle(self,request):
        while True:
            try:
                data_update.payer_transitions_data(request)
                data_update.imaging_studies_data(request)
                data_update.immunization_data(request)
                data_update.careplan_data(request)
                data_update.condition_data(request)
                data_update.organizations_data(request)
                data_update.encounter_data(request)
                data_update.devices_data(request)
                data_update.patients_data(request)
                data_update.allergies_data(request)

                # Log success message
                logging.info('Data update was successful.')
            except Exception as e:
                # Log error message
                logging.error(f'Data update failed: {str(e)}')

            # Pause script for 12 hours
            time.sleep(12 * 60 * 60)
