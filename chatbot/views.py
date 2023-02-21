from django.shortcuts import render,redirect
from django.apps import apps
from django.views import View
from .models import patients,procedure
import re
from django.db.models import Q
from .tests import finders,chat
from .updater import data_update
from datetime import datetime,date
from django.core.cache import cache

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
        cache.delete('chat_history')
        return render(request,'index.html')
    def post(self, request):
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

        # Retrieve chat history from cache
        chat_history = cache.get('chat_history', [])

        if len(find)>1:
            answer = chat.chatting(request,f"{text}, more than one")
        elif len(find)==1:
            answer = chat.chatting(request,f"{text}, found one")
        elif len(find)==0:
            for word in index.patt:
                    if re.search(word,text):
                        answer = chat.chatting(request,f"{text}, no one found")
                        break
        
        # Add new chat message to chat history in cache
        chat_history.append({'user': text, 'bot': answer, 'find':find})
        cache.set('chat_history', chat_history)

        data = {
            'ans':find,
            'len':len(find),
            'answer':answer,
            'chat_history': chat_history
        }

        # Redirect to next view after confirming patient
        yes_finder = finders.recognize_yes(text)
        if yes_finder == "yes":
            uid = request.POST.get('myInput')
            temp = finders.UUID(uid)
            if temp != None:
                url = f"/patient_chat/?uuid={temp}"
                return redirect(url)
        return render(request,'index.html',data)

class patient_chat(View):
    # Putting uuid of patient to url to get everytime
    def get(self,request):
        cache.delete('chat_history')
        p = "ok, what details do you want about patient"
        uuid = request.GET.get('uuid')
        patient = patients.objects.filter(
            Q(uuid =  uuid)
        )
        return render(request,'chat.html',{'uuid':uuid,'p':p,'patient':patient})
    def post(self,request):
        # try:

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

        #Patient data
        patient = patients.objects.filter(
            Q(uuid =  uuid)
        )
        
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

        #chat openai
        if len(y)!=0:
            if len(find)==0:
                reply = chat.data_chatting(request,f"{prompt}, No data found")
            else:
                reply = chat.data_chatting(request,f"{prompt}, data found")
        else:
            reply = chat.data_chatting(request,"other question")

        # Retrieve chat history from cache
        chat_history = cache.get('chat_history', [])
        # Add new chat message to chat history in cache
        chat_history.append({'user': prompt, 'bot': reply, 'find':final_find})
        cache.set('chat_history', chat_history)

    

        dt = {
            'patient':patient,
            'find':final_find,
            "y":y,
            "len":len(find),
            "reply":reply,
            "chat_history":chat_history
            }
        return render(request,'chat.html',dt)


# Currently not working
# View to show data as a table in brief 
class All_data(View):
    def get(self,request):
        return render(request, 'table.html')
    def post(self,request):
        uuid = 'fca3178e-fb68-41c3-8598-702d3ca68b96'
        prompt = request.POST.get('text')
        y = chat.find_model_names(prompt)
        model = apps.get_model('chatbot', y[0])
        find_data = model.objects.filter(
                    Q(patient =  f"['{uuid}']") | Q(patient =  uuid) 
                ).values()

        fields = [field.name for field in model._meta.get_fields()]

        headers = []

        for i in find_data:
            temp = []
            for k in fields:
                temp.append(i[k])
            headers.append(temp)


        dt = {
            'find':find_data,
            "y":y,
            "fields":fields,
            "heads":headers
            }
        return render(request,'table.html',dt)