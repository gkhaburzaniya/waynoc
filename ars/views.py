from django.shortcuts import render
from django.views import View


class Ars(View):
    template_name = "ars/ars.html"

    @classmethod
    def get(cls, request):
        return render(request, cls.template_name)
