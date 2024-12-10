from django.contrib import admin

# Register your models here.

from home.models import Settings, Language, SettingLang

from .models import ContactMessage


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status']
    list_filter = ['status']

class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['title', 'keywords', 'description', 'lang']
    list_filter = ['lang']


admin.site.register(Settings)
admin.site.register(ContactMessage)
admin.site.register(SettingLang, SettingLangAdmin)
admin.site.register(Language, LanguagesAdmin)










