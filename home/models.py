from django.db import models

# Create your models here.

from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Settings(models.Model):
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=100)
    description = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    smtp_server = models.CharField(max_length=30)
    smtp_email = models.CharField(max_length=30)
    smtp_password = models.CharField(max_length=30)
    smtp_port = models.CharField(max_length=30)
    youtube = models.CharField(max_length=30)
    instagram = models.CharField(max_length=30)
    facebook = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='images/')
    aboutus = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=30)
    phone = models.CharField(blank=True, max_length=30)
    subject = models.CharField(blank=True, max_length=30)
    message = models.TextField(blank=True, max_length=30)
    status = models.CharField(max_length=30, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=30)
    note = models.CharField(blank=True, max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'message': TextInput(attrs={'class': 'input', 'placeholder': 'Your message', 'rows': '5'}),
        }

class Language(models.Model):
    name = models.CharField(blank=True, max_length=30)
    code = models.CharField(blank=True, max_length=30)
    status = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

list = Language.objects.all()
list1 = []
for rs in list:
    list1.append((rs.code, rs.name))
langlist = (list1)


class SettingLang(models.Model):
    setting = models.ForeignKey(Settings, on_delete=models.CASCADE)
    lang = models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=100)
    description = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    smtp_server = models.CharField(max_length=30)
    smtp_email = models.CharField(max_length=30)
    smtp_password = models.CharField(max_length=30)
    smtp_port = models.CharField(max_length=30)
    youtube = models.CharField(max_length=30)
    instagram = models.CharField(max_length=30)
    facebook = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='images/')
    aboutus = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'






