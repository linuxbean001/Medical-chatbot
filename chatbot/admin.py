from django.contrib import admin
from .models import patients,condition,allergy,medication,careplan,device,encounter,payer_transitions
from .models import payers,procedure,provider,imaging_studies,immunization,observations,organizations,supplies

# Register your models here.
admin.site.register(patients)
admin.site.register(condition)
admin.site.register(allergy)
admin.site.register(medication)
admin.site.register(careplan)
admin.site.register(device)
admin.site.register(encounter)
admin.site.register(payer_transitions)
admin.site.register(payers)
admin.site.register(procedure)
admin.site.register(provider)
admin.site.register(imaging_studies)
admin.site.register(immunization)
admin.site.register(observations)
admin.site.register(organizations)
admin.site.register(supplies)