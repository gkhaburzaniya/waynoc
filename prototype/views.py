from django.shortcuts import render
from django.views import View


class Prototype(View):
    template_name = "prototype/prototype.html"

    @classmethod
    def get(cls, request):
        return render(request, cls.template_name)
