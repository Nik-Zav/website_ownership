from django.shortcuts import render, redirect
from .forms import AnalysisForm
from .utils.analysis import analyze_website_ownership
from django.urls import reverse


def index(request):
    """Главная страница приложения"""
    return render(request, 'index.html')


def analyze_website(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            org_data = {
                'name': form.cleaned_data['org_name'],
                'ogrn': form.cleaned_data['ogrn'],
                'phone': form.cleaned_data.get('phone'),
                'director_name': form.cleaned_data.get('director_name')
            }
            score, details = analyze_website_ownership(url, org_data)
            request.session['analysis_results'] = {
                'score': score,
                'details': details,
                'url': url,
                'org_name': org_data['name']
            }
            return redirect(reverse('ownership_checker:results'))
    form = AnalysisForm()
    return render(request, 'analysis_form.html', {'form': form})


def results_view(request):
    results = request.session.get('analysis_results', {})
    return render(request, 'results.html', results)
