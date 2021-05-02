from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings

from core.models import TelUser, Answer

import csv


class Result(View):
    """Generating Result for each User"""
    def get(self, request, chat_id):
        user = get_object_or_404(TelUser, chat_id=chat_id)
        elapsed = timezone.now() - user.date_joined
        days = elapsed.days

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
            'days': days,
            'qnum': day*2,
            'anum': len(answers),
            'yesnum': yesnum,
            'nonum': nonum,
            'nopercent': round((nonum/len(answers))*100),
            'time': notime,
        })


class AllRES(View):
    """All resulsts"""
    def get(self, request):
        users = get_list_or_404(TelUser)
        answers = get_list_or_404(Answer)

        for user in users:
            if user.chat_id == 305710135:
                users.remove(user)

        yesnum = nonum = day = night = 0
        for answer in answers:
            if answer.answer == 'NO':
                nonum += 1
                if answer.day_or_night() == "D":
                    day += 1
                else:
                    night += 1
            else:
                yesnum += 1
        _yesnum = round((yesnum/len(answers))*100)

        answersbydate, answersbydate2 = Answer.objects.all_by_date(jalali=True)
        nopercent = []
        nodays = []
        for ans in answersbydate2:
            noday = 0
            for a in ans:
                if a.answer == 'NO':
                    noday += 1
            nopercent.append(noday/len(ans))
            nodays.append(noday)

        maxdaypercent = max(nopercent)
        maxday = nopercent.index(maxdaypercent)
        maxday = answersbydate[maxday][0].date()

        mindaypercent = min(nopercent)
        minday = nopercent.index(mindaypercent)
        minday = answersbydate[minday][0].date()

        nopercent = sum(nopercent)/len(nopercent)

        notime = 'روز'
        if night > day:
            notime = 'شب'

        return render(request, 'stats/all.html', {
            'usersnum': len(users),
            'answersnum': len(answers),
            'yesnum': _yesnum,
            'nonum': 100 - _yesnum,
            'nopercent': round(nopercent*10),
            'maxday': maxday,
            'maxdaypercent': round(maxdaypercent*10),
            'minday': minday,
            'mindaypercent': round(mindaypercent*10),
            'notime': notime,
        })


class ReportCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        allbydate = Answer.objects.all_by_date(jalali=True)[0]
        row1 = [str(i[0].date()) for i in allbydate]
        try:
            if request.GET['jalali'] == '0':
                allbydate = Answer.objects.all_by_date(jalali=False)[0]
                row1 = [str(i[0]) for i in allbydate]
        except:
            allbydate = Answer.objects.all_by_date(jalali=True)[0]
            row1 = [str(i[0].date()) for i in allbydate]

        row2 = row3 = []
        for i in allbydate:
            counter = 0
            for j in i[1]:
                if j.answer == 'NO':
                    counter += 1
            avr = (counter/len(i[1]))*100
            row2.append(round(avr, 2))
            row3.append(avr/counter)

        row3 = [i for i in row2]

        writer = csv.writer(response)
        writer.writerow(row1)
        writer.writerow(row2)

        return response
