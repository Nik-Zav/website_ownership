from django import forms


class AnalysisForm(forms.Form):
    url = forms.URLField(label='URL сайта для анализа')
    org_name = forms.CharField(label='Название организации', max_length=255)
    ogrn = forms.CharField(label='ОГРН', max_length=13)
    phone = forms.CharField(label='Телефон', max_length=20, required=False)
    director_name = forms.CharField(
        label='ФИО руководителя',
        max_length=255, 
        required=False
    )