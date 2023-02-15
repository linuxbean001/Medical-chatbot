from django.shortcuts import render,redirect
from django.apps import apps
from django.views import View
from .models import patients,procedure
import re
from django.db.models import Q
from .tests import finders,chat
from .updater import data_update
from datetime import datetime,date

# Create your views here.

# Temprary function to test data updating functions
def updater(request):
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
    except Exception as e:
            # error message
            print(f'Data update failed: {str(e)}')
    return redirect('/')

# First upcoming View
class index(View):
    patt = ['\d{4}-\d\d-\d\d','\d{4}-\d-\d','\d{4}-\d-\d\d','\d{4}-\d\d-\d','\d{3}-\d\d-\d{4}','[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',]
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        # prompt from user
        text = request.POST.get('text')

        # Details in user input
        UUID = finders.UUID(text)
        DOB = finders.DOB(text)
        DOD = finders.DOD(text)
        SSN = finders.SSN(text)
        First = finders.first_name(text)
        Last = finders.last_name(text)

        # Fetching filtered data from django models
        if DOD is not None:
            find = patients.objects.filter(
                Q(deathdate = DOD, ssn = SSN) | Q(ssn = SSN) | Q(deathdate = DOD) |  Q(uuid = UUID) |Q(first = First, last = Last) | Q(first = First) | Q(last = Last) 
            )
        else:
            find = patients.objects.filter(
                Q(ssn = SSN) | Q(birthdate = DOB) | Q(birthdate = DOB, ssn = SSN) | Q(uuid = UUID) |Q(first = First, last = Last) | Q(first = First) | Q(last = Last)
                )

        # Creating reply for user by openai
        answer = chat.chatting(request,text)
        if len(find)>1:
            answer = chat.chatting(request,f"{text}, more than one")
        elif len(find)==1:
            answer = chat.chatting(request,f"{text}, found one")
        elif len(find)==0:
            for word in index.patt:
                    if re.search(word,text):
                        answer = chat.chatting(request,f"{text}, no one found")
                        break
                
        data = {
            'ans':find,
            'len':len(find),
            'answer':answer
        }

        # Redirect to next view after confirming patient
        yes_finder = finders.recognize_yes(text)
        if yes_finder == "yes":
            uid = request.POST.get('h1_value')
            temp = finders.UUID(uid)
            if temp != None:
                url = f"/patient_chat/?uuid={temp}"
                return redirect(url)

    
        return render(request,'index.html',data)

class patient_chat(View):
    # Putting uuid of patient to url to get everytime
    def get(self,request):
        p = "ok, what details do you want about patient"
        uuid = request.GET.get('uuid')
        return render(request,'chat.html',{'uuid':uuid,'p':p})
    def post(self,request):
        try:

            # Getting uuid and user input
            uuid = request.GET.get('uuid')
            prompt = request.POST.get('text')

            # to understan users sentences timings and confirming model
            time = finders.determine_time_frame(prompt)
            y = chat.find_model_names(prompt)

            with_stop = ['allergy','careplan','condition','device','encounter','medication']
            with_date = ['imaging_studies','immunization','observations','procedure']
            find = []
            final_find = []
            
            #Fetching filtered daa
            for i in y:
                model = apps.get_model('chatbot', i)
                find_data = model.objects.filter(
                        Q(patient =  f"['{uuid}']") | Q(patient =  uuid) 
                    )
                find.extend(find_data)

                #Filtering fetched data again 
                if  i in with_stop:
                    if time == 1 or time == 2:
                        final_find = [f for f in find if f.stop==None]
                    elif time == 0:
                        final_find = [f for f in find if f.stop is not None]
                    else:
                        final_find = find
                elif  i in with_date:
                    if time == 1 or time == 2:
                        final_find = [f for f in find if f.date.timestamp() >= datetime.today().timestamp()]
                    elif time == 0:
                        final_find = [f for f in find if f.date.timestamp() < datetime.today().timestamp()]
                    else:
                        final_find = find
            
                #  getattr(obj, field_name)


            headers = []
            if len(find) > 0:
                for field in find[0]._meta.fields:
                    headers.append(field.name)
            


            #chat openai
            if len(y)!=0:
                if len(find)==0:
                    reply = chat.data_chatting(request,f"{prompt}, No data found")
                else:
                    reply = chat.data_chatting(request,f"{prompt}, data found")
            else:
                reply = chat.data_chatting(request,"other question")

            dt = {
                'find':final_find,
                "y":y,
                "len":len(find),
                "reply":reply,
                "headers":headers,
                }
        except:
            return redirect('/')
        return render(request,'chat.html',dt)


# Currently not working
# View to show data as a table in brief 
class All_data(View):
    def get(self,request):
        return render(request, 'table.html')
    def post(self,request):
        uuid = 'fc817953-cc8b-45db-9c85-7c0ced8fa90d'
        prompt = request.POST.get('text')
        y = chat.find_model_names(prompt)
        model = apps.get_model('chatbot', y[0])
        find_data = model.objects.filter(
                    Q(patient =  f"['{uuid}']") | Q(patient =  uuid) 
                )
        
        heads = []
        headers = model._meta.get_fields()
        # for field in fields:
        #     field_name = field.name
        #     # now you can use the field name as an attribute of a model instance
        #     obj1 = model.objects.first()
        #     value = getattr(obj1, field_name)

        dt = {
            'find':find_data,
            "y":y,
            "headers":headers,
            "heads":heads
            }
        return render(request,'table.html',dt)