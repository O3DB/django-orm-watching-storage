from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode = passcode)
    passcard_visits = Visit.objects.filter(passcard = passcard)
    
    this_passcard_visits = []
    now = timezone.now()
    
    for visit in passcard_visits:
        if visit.leaved_at:
            duration = visit.leaved_at - visit.entered_at
        else:
            duration = now - visit.entered_at
        is_strange = duration.seconds >= 3600
        this_passcard_visits.append({
            "date": visit.entered_at,
            "duration": duration,
            "is_strange": is_strange,
        })

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits,
    }
    return render(request, 'passcard_info.html', context)
