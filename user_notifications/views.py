from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
class ReminderConfirmation(View):

    def post(self, request, *args, **kwargs):
        return redirect()

class ReminderDecline(View):

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return redirect()