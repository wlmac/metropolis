from django.shortcuts import render

def calendar(request):
    return render(request, "core/calendar/view.html")