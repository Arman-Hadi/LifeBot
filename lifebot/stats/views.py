from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.utils import timezone

from core.models import TelUser, Answer


class Result(View):
    """Generating Result for each User"""
    def get(self, request, chat_id):
        user = get_object_or_404(TelUser, chat_id=chat_id)

        elapsed = timezone.now() - user.date_joined
        minute, second = divmod(elapsed.seconds, 60)
        hour, minute = divmod(minute, 60)
        year, day = divmod(elapsed.days, 365)
        del year, hour, minute, second


        yesnum = nonum = day = night = 0
        answers = get_list_or_404(Answer, user=user)
        for answer in answers:
            if answer.answer == 'YS':
                yesnum += 1
            else:
                nonum += 1
                if answer.day_or_night() == "D":
                    day += 1
                else:
                    night += 1

        notime = 'روز'
        if night > day:
            notime = 'شب'

        return render(request, 'stats/result.html', {
            'name': user.first_name,
            'days': day,
            'qnum': day*2,
            'anum': len(answers),
            'yesnum': yesnum,
            'nonum': nonum,
            'nopercent': round((nonum/len(answers))*100),
            'time': notime,
        })
