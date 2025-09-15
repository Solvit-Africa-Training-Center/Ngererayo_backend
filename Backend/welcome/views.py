from django.shortcuts import render
from django.views import View





class ApiLandingPageView(View):
    def get(self, request):
        return render(request, 'ApiLandingPage.html')
# Create your views here.
