from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist  # This may be used instead of Users.DoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from .medget import medget
from django.views import generic
from django.db import IntegrityError
import re
from main import medplace
from django.urls import reverse
# for older versoins of Django use:
# from django.core.urlresolvers import reverse
import ast
import datetime
import time

from .models import Users, History
from main.forms import SignupForm, LoginForm, SearchForm  # ,AddTopicForm,AddOpinionForm,

ob = medget()
j = []


def index(request):
        return render(request, 'Temp/index.html')

def aboutus(request):
        return render(request, 'Temp/about.html')

def gallery(request):
        return render(request, 'Temp/gallery.html')

def contactus(request):
        return render(request,'Temp/contact.html')

def checknow(request):
    if request.session.has_key('user_id'):
        uid = request.session['user_id']
        try:
            user = Users.objects.get(pk=uid)
            hist = []
            hist.extend(History.objects.filter(email=user.email).values('dis_name', 'dis_severity', 'dis_time'))
            # return HttpResponse(hist)
            return render(request, 'Temp/symptomdash.html', {'user_id': user, 'history': hist})
        except Users.DoesNotExist:
            return HttpResponse("UserName not found")
    else:
        return render(request, 'Temp/signupform.html')

def reports(request):
    if request.session.has_key('user_id'):

        uid = request.session['user_id']
        try:
            user = Users.objects.get(pk=uid)
            hist = []
            hist.extend(History.objects.filter(email=user.email).values('dis_name', 'dis_severity', 'dis_time'))
            # return HttpResponse(hist)
            return render(request, 'Temp/reports.html', {'user_id': user, 'history': hist})
        except Users.DoesNotExist:
            return HttpResponse("UserName not found")


def login(request):
    return HttpResponseRedirect(reverse('main:checknow'))




def search_checkup(request):
    return render(request, 'Temp/search_checkup.html')




def search(request):
    if request.method == 'POST':
        topic = SearchForm(request.POST)
        if topic.is_valid():

            # t=Topic.objects.get(topic_text=topic.cleaned_data.get('topic_text'))
            top_li = Topic.objects.all()
            li = []
            for t in top_li:
                if re.search(topic.cleaned_data.get('topic_text'), t.topic_text, re.IGNORECASE):
                    li.append(t)
            if request.session.has_key('user_id'):
                uid = request.session['user_id']
                user = Users.objects.get(pk=uid)
                return render(request, 'Temp/searchresults.html', {'user_id': user, "list": li})
            else:
                return render(request, 'Temp/searchresultL.html', {"list": li})
        else:
            return HttpResponse("Form not valid")
    else:
        return HttpResponse("not POST")


def search1(request):
        
        topic = SearchForm(request.POST, initial={"topic_text": "c"})
        if topic.is_valid():
            sim_str = topic.cleaned_data.get('topic_text')
            checklist = sim_str.split(",")
            # checklist = topic.cleaned_data.get('symptom')
            try:
                checklist.append(request.POST['symptom1'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom2'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom3'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom4'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom5'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom6'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom7'])
            except:
                pass
            # return HttpResponse(checklist)


            li = ob.search_symptoms(checklist)

            l = len(li)
            return render(request, 'Temp/request2.html', {"list": li, "len": l})


            # return HttpResponse((' ').join(li))
            # t=Topic.objects.get(topic_text=topic.cleaned_data.get('topic_text'))

        else:
            return HttpResponse(topic.errors)



def register(request):
    try:
        if request.method == 'POST':
           
            em=str(request.POST['email'])
            pw=str(request.POST['pwd'])
            p = Users(email=em,pwd=pw)
            p.save()
            return HttpResponseRedirect(reverse('main:login'))
    except IntegrityError:
        return HttpResponse("You are already registered.")




def logInReq(request):
    if request.method == 'POST':
        log = LoginForm(request.POST)
        if log.is_valid():
            try:
                em=log.cleaned_data.get('email')
                pw=log.cleaned_data.get('pwd')
                user = Users.objects.get(email = em,pwd = pw)
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('main:checknow'))
            except Users.DoesNotExist:
                return HttpResponse("WRONG USERNAME OR PASSWORD")


"""
class LoggedIn(generic.DetailView):
	model = Users
	template_name = 'Temp/logged.html'
	context_object_name = 'user_id'
"""


def quest(request):

    global ob
    if request.method == 'POST':
        l = request.POST['len']
        checklist = []
        for i in range(int(l)):
            try:
                checklist.append(request.POST['symptom' + str(i)])
            except:
                pass
        # return HttpResponse(checklist)
        if request.session.has_key('user_id'):
            uid = request.session['user_id']
            try:
                user = Users.objects.get(pk=uid)
            except ObjectDoesNotExist:
               return render(request,'Temp/index.html')

            age = request.session['age']
            sex = request.session['sex']
            print("calling get dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            ob.get_data(sex, age)
            print("return         calling get dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            lis = []
            for i in checklist:
                dic = {}
                dic['id'] = i
                dic['status'] = 'present'
                lis.append(dic)
                dic = None

            # ob.add_symptoms(lis)
            request.session['lis'] = lis
            return HttpResponseRedirect(reverse('main:question'))
            # return HttpResponse(a)
            # ob.get_questions()


def question(request):

    global ob
    # global j
    # j +=1
    i = []
    age = request.session['age']
    sex = request.session['sex']
    ob.get_data(sex, age)
    if request.session.has_key('lis'):
        i = request.session['lis']
        print(" im culprit 1")
        ob.add_symptoms(i)
        a = ob.get_question()
        return render(request, 'Temp/myquestion.html', {"ques_dict": a})
        # return HttpResponse(a)
    elif not ob.check_risk():
        i = {}
        # id = request.POST.get('id')
        if request.POST.get('yes'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'present'
        elif request.POST.get('no'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'absent'
        elif request.POST.get('dont'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'unknown'

        a = []
        a.append(i)
        print("i am culprit 2222")
        ob.add_symptoms(a)
        a = ob.get_question()
        # j = i
        return render(request, 'Temp/myquestion.html', {"ques_dict": a})
    else:
        result = {}
        uid = request.session['user_id']
        user = Users.objects.get(pk=uid)
        result = ob.get_result()
        History(
            email=user.email,
            dis_name=result['name'],
            dis_severity=result['severity'],
            dis_probname="",
            dis_hint=result['hint'],
            dis_time=str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')),
        ).save()
        return render(request, 'Temp/myresult.html', {"result": result})


def doc_list(request):
    #location = request.POST['location']
    #loc_dict = ast.literal_eval(location)
    loc_dict1 = {}
    try:
        loc_dict1['lat'] = request.COOKIES.get('latitude')
    except:
        loc_dict1['lat'] = loc_dict['latitude'] #request.COOKIES.get('latitude')
    try:
        loc_dict1['lng'] = request.COOKIES.get('longitude')
    except:
        loc_dict1['lng'] = loc_dict['longitude'] #request.COOKIES.get('longitude')
    doctor_type = request.POST['doctor_type']
    doctor = doctor_type.split()
    doctor_search = doctor[-2] + doctor[-1]
    plac = medplace.get_places(lat_lng=loc_dict1, doctor_type=doctor_search)
    return render(request, 'Temp/doctor.html', {"doc_list": plac})


def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    return HttpResponseRedirect(reverse('main:index'))


def ajaxreq(request):
    return render(request, 'Temp/request0.html')

def basicsymptoms(request):
    sex = request.GET['sex']
    age = request.GET['age']
    request.session['sex'] = sex
    request.session['age'] = age
    return render(request, 'Temp/request1.html')


        # return HttpResponse((' ').join(li))
        # t=Topic.objects.get(topic_text=topic.cleaned_data.get('topic_text'))
def bum(request):
    topic = SearchForm(request.GET, initial={"topic_text": "c"})
    sim_str = topic.cleaned_data.get('topic_text')
    checklist = sim_str.split(",")
    # checklist = topic.cleaned_data.get('symptom')
    try:
        checklist.append(request.POST['symptom1'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom2'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom3'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom4'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom5'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom6'])
    except:
        pass
    try:
        checklist.append(request.POST['symptom7'])
    except:
        pass
    # return HttpResponse(checklist)

    li = ob.search_symptoms(checklist)

    l = len(li)
    return render(request, 'Temp/request2.html', {"list": li, "len": l})
