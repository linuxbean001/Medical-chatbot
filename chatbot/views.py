from django.shortcuts import render,redirect
from django.apps import apps
from django.views import View
from .models import patients
import re
from django.db.models import Q
from .tests import finders,chat
from datetime import datetime,date
from django.core.cache import cache
from django.utils.timezone import get_fixed_timezone



# Create your views here.


# First upcoming View


class index(View):
    patt = ['\d{4}-\d\d-\d\d','\d{4}-\d-\d','\d{4}-\d-\d\d','\d{4}-\d\d-\d','\d{3}-\d\d-\d{4}','[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}']
    normal = ['patient',"hii","hello","Hii","Hello","HII","HELLO"]
    def get(self,request):
        cache.delete('chat_history')
        return render(request,'index.html')
    def post(self, request):
        # prompt from user
        text = request.POST.get('text')

        # Details in user input
        UUID = finders.UUID(text)
        DOB = finders.DOB(text)
        print(DOB)
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

        # Redirect to next view after confirming patient
        yes_finder = finders.recognize_yes(text)
        if yes_finder == "yes":
            uid = request.POST.get('myInput')
            temp = finders.UUID(uid)
            if temp != None:
                url = f"/patient_chat/?uuid={temp}"
                return redirect(url)
        

        # Retrieve chat history from cache
        chat_history = cache.get('chat_history', [])

        if len(find)>1:
            answer = chat.chatting(request,f"{text}, more than one")
        elif len(find)==1:
            answer = chat.chatting(request,f"{text}, found one")
        else:
            checker = [word for word in index.patt if re.search(word,text)]
            ungeneral = [word for word in index.normal if re.search(word,text)]
            if len(checker)>0:
                answer = chat.chatting(request,f"{text}, no one found")
            elif len(ungeneral)>0:
                answer = chat.chatting(request,text)
            else:
                answer = chat.general_chat(text)
        
        # Add new chat message to chat history in cache
        chat_history.append({'user': text, 'bot': answer, 'find':find})
        cache.set('chat_history', chat_history)

        data = {
            'ans':find,
            'len':len(find),
            'answer':answer,
            'chat_history': chat_history
        }

        
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
        date = finders.DOB(prompt)
        print(date)

        # to understan users sentences timings and confirming model
        time = finders.determine_time_frame(prompt)
        m = chat.find_model_names(prompt)
        if len(m)>0:
            y = m[0]
        else:
            y = None

        with_stop = ['allergy','careplan','condition','device','encounter','medication']
        with_date = ['imaging_studies','immunization','observations','procedure']
        final_find = []

        #Patient data
        patient = patients.objects.filter(
            Q(uuid =  uuid)
        )
        
        #Fetching filtered daa
        if y:
            model = apps.get_model('chatbot', y)
            find = model.objects.filter(
                    Q(patient =  f"['{uuid}']") | Q(patient =  uuid) 
                )


        #Filtering fetched data again 
        if  y in with_stop:
            if time == 1 or time == 2:
                final_find = [f for f in find if f.stop==None]
            elif time == 0:
                final_find = [f for f in find if f.stop is not None]
            elif time == 3:
                if date is not None:
                    final_find = [f for f in find if f.start.timestamp()==date.timestamp()]
                else:
                    final_find = find
            else:
                final_find = find
        elif  y in with_date:
            if time == 1 or time == 2:
                final_find = [f for f in find if f.date.timestamp() >= datetime.today().timestamp()]
            elif time == 0:
                final_find = [f for f in find if f.date.timestamp() < datetime.today().timestamp()]
            elif time == 3:
                if date is not None:
                    final_find = [f for f in find if f.date.date() == datetime.strptime(date, "%Y-%m-%d").date()]
                else:
                    final_find = find
            else:
                final_find = find
        
        else:
            final_find = find

        #chat openai
        if y:
            if len(final_find) > 0:
                reply = chat.data_chatting(request, prompt)
            else:
                reply = chat.no_data_found(request, prompt)
        else:
            reply = chat.general_chat(prompt)

        # Retrieve chat history from cache
        chat_history = cache.get('chat_history', [])
        # Add new chat message to chat history in cache
        chat_history.append({'user': prompt, 'bot': reply, 'find':final_find})
        cache.set('chat_history', chat_history)
        
        # except:
        #     return redirect('/')

    

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
