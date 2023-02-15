from django.test import TestCase
from datetime import datetime
import openai
import re
import nltk
from nltk.corpus import wordnet
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from .gp import GPT,Example

# Create your tests here.

# all functions for chatting
class chat:

    model_map = {
        'condition': ['condition', 'conditions', "condit", 'illness', 'ailment', 'disease', 'disorder', 'affliction', "prognosis"],
        'allergy': ['allergy', 'allergies', 'hypersensitivity', 'reaction', 'sensitivity', 'intolerance',"aller"],
        'medication': ['medication', 'medications', 'prescription', 'drug', 'medicine', 'pharmaceutical', 'remedy', "treatment", "treatment plan"],
        'careplan': ['careplan', 'careplans', 'plan', 'strategy', 'scheme', 'approach', 'course of action'],
        'device': ['device', 'devices', 'apparatus', 'machine', 'gadget', 'instrument', 'equipment'],
        'encounter': ['encounter', 'encounters', 'meeting', 'interaction', 'encounter', 'visit', 'appointment'],
        'procedure': ['procedure', 'procedures', 'surgery', 'operation', 'procedure', 'technique', 'process'],
        'imaging_studies': ['imaging_studies', 'scans', 'test', 'imaging', 'studies', 'examination', 'examinations'],
        'immunization': ['immunization', 'immunizations', 'vaccination', 'injection', 'immunization', 'shot', 'jab'],
        'observations': ['observation','observe', 'notes', 'comments', 'observations', 'records', 'documentation'],
        # 'organizations': ['organizations', 'companies', 'firms', 'organizations', 'agencies', 'institutions'],
        # 'supplies': ['supplies', 'goods', 'products', 'items', 'supplies', 'materials']
        # 'payer_transitions': ['payer_transitions', 'transitions', 'shifts', 'changes', 'alterations'],
        # 'payers': ['payer', 'insurers', 'providers', 'payers', 'financiers', 'sponsors'],
        # 'provider': ['provider', 'providers', 'doctor', 'physician', 'caregiver', 'practitioner', 'professional'],
        }


    def find_model_names(sentence):
        result = []
        for model_name, synonyms in chat.model_map.items():
            for word in synonyms:
                if re.search(word, sentence):
                    result.append(model_name)
                    break
        return result

    # Openai function to reply users question in first View
    def chatting(self,prompt):
        openai.api_key = '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'


        # model to generate the answer
        gpt = GPT(engine="davinci",
                temperature=0.2,
                max_tokens=100)


        gpt.add_example(Example('hello'or'hii'or'namaste'or'hi','hii how can i help you'))
        gpt.add_example(Example("i am searching for a patient","Sure do you have some details about patient like his dob, ssn or uuid"))
        gpt.add_example(Example('i need some details about a patient','Ya sure tell me patient SSN no. or some other details like DOB'))
        gpt.add_example(Example('give me details about the patient whose dob is 2022-04-11 and ssn 9876-32-4342, no one found','Sorry there is no such patient, Please check details once again or try with some different details'))
        gpt.add_example(Example('give me details about the patient whose dob is 2022-04-11, more than one','which one are you talking about Please confirm with SSN no.'))
        gpt.add_example(Example('I have patient uuid 6d048a56-edb8-4f29-891d-7a84d75a8e78, found one','Is this the patient you are searching for please confirm yes or no'))
        gpt.add_example(Example('yes that was the patient','Please give his ssn no. again'))
        gpt.add_example(Example('6d048a56-edb8-4f29-891d-7a84d75a8e78, found one','please confirm if this is the patient you are talking about by saying yes'))
        gpt.add_example(Example('can you find the patient whose dob is 1914-09-05 and ssn is 999-72-8988, more than one','Which one are you talking about please confirm with ssn no.'))
        p = gpt.submit_request(prompt)
    
        return p['choices'][0]['text'][8:]
    
    # another Openai function to reply in patient_chat View
    def data_chatting(self,prompt):
        openai.api_key = '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'
        kpt = GPT(engine="davinci",
                temperature=0.2,
                max_tokens=100)

        kpt.add_example(Example("Tell me about the patients medications, data found","This is The Data avaliable about patients Medication"))
        kpt.add_example(Example("Tell me about the patients observation ,No data found","Sorry I don't have any data about patients Observations"))
        kpt.add_example(Example("Tell me about the patients observation, data found","There are Patient Observations"))
        kpt.add_example(Example("other question","Please click on Restart if you want to ask questions about other patient or context"))

        p = kpt.submit_request(prompt)
    
        return p['choices'][0]['text'][8:]


# All functions to find details from users sentences
class finders:

    time_frame_map = {
        0: ['past', 'previous', 'before', 'ago', 'yesterday', 'last', 'earlier', 'history', 'former', 'old'],
        1: ['present', 'now', 'currently', 'current', 'today', 'this', 'moment', 'time', 'instant', 'ongoing', 'here and now'],
        2: ['future', 'after', 'next', 'later', 'tomorrow', 'henceforth', 'upcoming', 'subsequently', 'soon', 'forthcoming']
    }

    #Finds timings from user inputs
    def determine_time_frame(user_input):
        words = set(word_tokenize(user_input.lower()))
        for time_frame, keywords in finders.time_frame_map.items():
            if any(word in words for word in keywords):
                return time_frame
        return 3

    # to change date format yy-mm-dd sothat able to be matched
    def change_date_format(date_str):
        parts = date_str.split("-")
        return "{}-{}-{}".format(parts[2], parts[1], parts[0])

    # Date finder
    def DOB(text):
        patterns = '\d{4}-\d\d-\d\d|\d{4}-\d-\d|\d{4}-\d-\d\d|\d{4}-\d\d-\d'
        patterns_2 = ' \d\d-\d\d-\d{4} | \d-\d\d-\d{4} | \d\d-\d-\d{4} | \d-\d-\d{4} '
        ans = re.findall(patterns,text)
        ans_2 = re.findall(patterns_2,text)
        new_ans_2 = [finders.change_date_format(x) for x in ans_2]
        f_ans = ans + new_ans_2
        if len(f_ans) == 0:
            return None
        return f_ans[0]

    def SSN(text):
        patterns = '\d{3}-\d\d-\d{4}'
        ans = re.findall(patterns,text)
        if len(ans) == 0:
            return None
        return ans[0]

    def UUID(text):
        patterns = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        ans = re.findall(patterns,text)
        if len(ans) == 0:
            return None
        return ans[0]
    
    # if user tries to search for a dead patient with deathdate
    def DOD(text):
        word = ['death','expired','dead','expire',"deceased", "passed away", "departed","DOD","dod","passed","died","Succumbed","Laid to rest"]
        death_pattern = re.compile(r"\b({})\b".format("|".join(word)))
        death_match = death_pattern.search(text)
        if death_match:
            patterns = '\d{4}-\d\d-\d\d|\d{4}-\d-\d|\d{4}-\d-\d\d|\d{4}-\d\d-\d'
            patterns_2 = ' \d\d-\d\d-\d{4} | \d-\d\d-\d{4} | \d\d-\d-\d{4} | \d-\d-\d{4} '
            ans = re.findall(patterns,text)
            ans_2 = re.findall(patterns_2,text)
            new_ans_2 = [finders.change_date_format(x) for x in ans_2]
            f_ans = ans + new_ans_2
            if len(f_ans) == 0:
                return None
            return f_ans[-1]
        else:
            return None
    
    # First name and Last name finders are not working quite well 
    def first_name(sentence):
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        named_entities = ne_chunk(tagged_words)
        
        for entity in named_entities:
            if hasattr(entity, 'label'):
                if entity.label() == 'PERSON':
                    return entity[0][0]
        return None

    def last_name(sentence):
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        named_entities = ne_chunk(tagged_words)
        
        for entity in named_entities:
            if hasattr(entity, 'label'):
                if entity.label() == 'PERSON':
                    return entity[-1][0]
        return None   

    # Finds yes in users sentence
    def recognize_yes(sentence):
        yes_words = ["yes", "yeah", "yup", "yep", "sure", "ok", "okay", "of course", "absolutely", "definitely"]
        sentence = sentence.lower()
        for word in yes_words:
            if re.search(word, sentence):
                return "yes"
        return "no"

    def find_words(text, word):
        word_synonyms = []
        word_lemmas = wordnet.lemmas(word)
        for lemma in word_lemmas:
            word_synonyms += [syn.name() for syn in lemma.synonyms()]

        for synonym in word_synonyms:
            if synonym in text:
                return True
        return False









