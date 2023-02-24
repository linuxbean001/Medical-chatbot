import requests
import json
from datetime import datetime,timedelta
from .models import patients,condition,allergy,medication,device,encounter,payer_transitions,careplan
from .models import payers,procedure,provider,imaging_studies,immunization,observations,organizations,supplies



class data_update:
    def condition_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblHIUNregfRjRK4n?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = condition(
                        start = fields.get('START', None),
                        stop = fields.get('STOP', None),
                        patient = fields.get('Id (from PATIENT)', None),
                        encounter = fields.get('Id (from ENCOUNTER)', None),
                        code = fields.get('CODE', None),
                        description = fields.get('DESCRIPTION', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Condition Table updated successfully"
            else:
                # Handle error
                m = 'condition table updatation failed'
        return m


    def patients_data(request):
        patients.objects.all().delete()
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblPyaClCdeoPiALK?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'medical',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = patients(
                        uuid = fields.get('Id', None),
                        birthdate = fields.get('BIRTHDATE',"0000-00-00"),
                        ssn = fields.get('SSN', None),
                        first = fields.get('FIRST', None),
                        last = fields.get('LAST', None),
                        race = fields.get('RACE', None),
                        ethnicity = fields.get('ETHNICITY', None),
                        gender = fields.get('GENDER', None),
                        birthplace = fields.get('BIRTHPLACE', None),
                        address = fields.get('ADDRESS', None),
                        city = fields.get('CITY', None),
                        state = fields.get('STATE', None),
                        county = fields.get('COUNTY', None),
                        lat = fields.get('LAT', None),
                        lon = fields.get('LON', None),
                        healthcare_expenses = fields.get('HEALTHCARE_EXPENSES', None),
                        healthcare_coverage = fields.get('HEALTHCARE_COVERAGE', None),
                        suffix = fields.get('SUFFIX', None),
                        prefix = fields.get('PREFIX', None),
                        maiden = fields.get('MAIDEN', None),
                        marital = fields.get('MARITAL', None),
                        drivers = fields.get('DRIVERS', None),
                        passport = fields.get('PASSPORT', None),
                        zip = fields.get('ZIP', None)
                    )
                    if 'DEATHDATE' in fields:
                        model_instance.deathdate = fields['DEATHDATE']
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Patients Table updated successfully"
            else:
                # Handle error
                m = 'Patients table updatation failed'
        return m

    def devices_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblRAqeq7FYjvk5eG?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = device(
                        start = fields.get('START', None),
                        stop = fields.get('STOP', None),
                        patient = fields.get('Id (from PATIENT)', None),
                        encounter = fields.get('Id (from ENCOUNTER)', None),
                        code = fields.get('CODE', None),
                        description = fields.get('DESCRIPTION', None),
                        udi = fields.get('UDI', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Device Table updated successfully"
            else:
                # Handle error
                m = "Devide Table updatation failed"
        return m
    
    def imaging_studies_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblyGtf8iy8jH4R2G?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):
                    
                    # Create Django model instance
                    model_instance = imaging_studies(
                        uuid = fields.get('Id', None),
                        date = fields.get('DATE', None),
                        patient = fields.get('Id (from PATIENT)', None),
                        encounter = fields.get('Id (from ENCOUNTER)', None),
                        body_site_code = fields.get('BODYSITE_CODE', None),
                        body_site_description = fields.get('BODYSITE_DESCRIPTION', None),
                        modality_code = fields.get('MODALITY_CODE', None),
                        modality_description = fields.get('MODALITY_DESCRIPTION', None),
                        sop_code = fields.get('SOP_CODE', None),
                        sop_description = fields.get('SOP_DESCRIPTION', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Imaging Table updated successfully"
            else:
                # Handle error
                m = "Imaging Table updatation failed"
        return m
    
    def immunization_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tbl4yFOsp2hK7rq54?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = immunization(
                        date = fields.get('DATE', None),
                        patient = fields.get('Id (from PATIENT)', None),
                        encounter = fields.get('Id (from ENCOUNTER)', None),
                        code = fields.get('CODE', None),
                        description = fields.get('DESCRIPTION', None),
                        base_cost = fields.get('BASE_COST', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Immunization Table updated successfully"
            else:
                # Handle error
                m = "Immunization Table updatation failed"
        return m

    def organizations_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tbljQjqxWTb6oTWs8?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = organizations(
                        uuid = fields.get('Id', None),
                        name = fields.get('NAME', None),
                        address = fields.get('ADDRESS', None),
                        city = fields.get('CITY', None),
                        state = fields.get('STATE', None),
                        zip = fields.get('ZIP', None),
                        lat = fields.get('LAT', None),
                        lon = fields.get('LON', None),
                        revenue = fields.get('REVENUE', None),
                        utilization = fields.get('UTILIZATION', None),
                        phone = fields.get('PHONE', None),
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Organizations Table updated successfully"
            else:
                # Handle error
                m = "Organizations Table updatation failed"
        return m

    def allergies_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblblFy59vNQVMgIj?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = allergy(
                        start = fields.get('START', None),
                        stop = fields.get('STOP', None),
                        patient = fields.get('Id (from PATIENT)', None),
                        encounter = fields.get('Id (from ENCOUNTER)', None),
                        code = fields.get('CODE', None),
                        description = fields.get('DESCRIPTION', None),
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Allergies Table updated successfully"
            else:
                # Handle error
                m = "Allergies Table updatation failed"
        return m

    def careplan_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblZLso3DDaZKZuHU?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = careplan(
                        uuid=fields.get('Id', None),
                        start=fields.get('START', None),
                        stop=fields.get('STOP', None),
                        patient=fields.get('Id (from PATIENT)', None),
                        encounter=fields.get('Id (from ENCOUNTER)', None),
                        code=fields.get('CODE', None),
                        description=fields.get('DESCRIPTION', None),
                        reason_code=fields.get('REASONCODE', None),
                        reason_description=fields.get('REASONDESCRIPTION', None),
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Careplan Table updated successfully"
            else:
                # Handle error
                m = "Careplan Table updatation failed"
        return m

    def encounter_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tblVYZitGwMiZb9Ch?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
                
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = encounter(
                        uuid = fields.get('Id', None),
                        start = fields.get('START', None),
                        stop = fields.get('STOP', None),
                        patient = fields.get('PATIENT', None),
                        organization = fields.get('ORGANIZATION', None),
                        provider = fields.get('PROVIDER', None),
                        payer = fields.get('PAYER', None),
                        encounter_class = fields.get('ENCOUNTER_CLASS', None),
                        code = fields.get('CODE', None),
                        description = fields.get('DESCRIPTION', None),
                        base_encounter_cost = fields.get('BASE_ENCOUNTER_COST', None),
                        total_claim_cost = fields.get('TOTAL_CLAIM_COST', None),
                        payer_coverage = fields.get('PAYER_COVERAGE', None),
                        reason_code = fields.get('REASON_CODE', None),
                        reason_description = fields.get('REASON_DESCRIPTION', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Encounter Table updated successfully"
            else:
                # Handle error
                m = "Encounter Table updatation failed"
        return m


    def payer_transitions_data(request):
        offset = 0
        while (offset != None):
            # Airtable API endpoint to retrieve data
            airtable_api_endpoint = f"https://api.airtable.com/v0/appC0KDqiur60vI3i/tbljYePvQXl1YF1yP?offset={offset}"
            # Airtable API key
            api_key = 'pat4nbJPk11OO5z8P.1d38cd34c62e82cd065caa8ee05735be9769a4fa49864a0dac0c14f09d2cf79e'

            # Request headers
            headers = {
                'Authorization': 'Bearer ' + api_key,
                'Content-Type': 'application/json'
            }

            # Request parameters
            params = {
                'view': 'Grid view',
            }

            # Get data from Airtable API
            response = requests.get(airtable_api_endpoint, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.content.decode('utf-8'))

                # Loop through records
                for record in data['records']:
                    # Extract record fields
                    fields = record['fields']

                    # created_time_str = record['createdTime']
                    # created_time = datetime.fromisoformat(created_time_str[:-1])

                    # # Check if the record was created within the last 12 hours
                    # if datetime.now() - created_time < timedelta(hours=12):

                    # Create Django model instance
                    model_instance = payer_transitions(
                        patient = fields.get('PATIENT', None),
                        start_year = fields.get('START_YEAR', None),
                        end_year = fields.get('END_YEAR', None),
                        payer = fields.get('PAYER', None),
                        ownership = fields.get('OWNERSHIP', None)
                    )
                    model_instance.save()

                    if "offset" in data:
                        offset = data["offset"]
                    else:
                        offset = None

                # Return success message
                m = "Patient_transiction Table updated successfully"
            else:
                # Handle error
                m = "Patient_transiction Table updatation failed"
        return m

    