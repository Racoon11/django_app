from django.contrib import admin
from .models import BaseEng, BaseGerm, UserWordEng, UserWordGerm


admin.site.register(BaseEng)
admin.site.register(BaseGerm)
admin.site.register(UserWordEng)
admin.site.register(UserWordGerm)
