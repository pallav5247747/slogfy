from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Apply_form, RegForm, login_form, adddata, jobForm
from .models import Job, Mcq, Apply
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

def sign_up(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.is_staff = True
            data.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password,is_staff = True)
            login(request, account)
            return redirect("admin")
        else:
            return render(request, "page/signup.html", {"form": RegForm(request.POST)})
    login_data = {
        "form": RegForm(),
    }
    return render(request, "page/signup.html", login_data)

def logout_view(request):
    logout(request)
    return redirect("admin")

def login_view(request, *args, **kwaegs):
    user = request.user
    if user.is_authenticated:
        return redirect("admin")
    if request.POST:
        form = login_form(request.POST)
        email = request.POST['email']
        raw_password = request.POST['password']
        account = authenticate(email=email, password=raw_password)
        if account is not None and account.is_staff == True:
            login(request, account)
            return redirect("admin")
        else:
            return render(request, "page/login.html", {"form": login_form(), "nologin": f" Email id or Password is incorrect"})
    return render(request, "page/login.html", {"form": login_form()})

# @login_required(login_url='/login/')
def home(request):
    con = {
        "data": Job.objects.all()
    }
    return render(request, "page/home.html", con)

@login_required(login_url='/login/')
def admin(request):
    data = Apply.objects.all()
    return render(request, "page/admin_main.html", {"data": data})

@login_required(login_url='/login/')
def hire(request, id):
    data = Apply.objects.get(pk=id)
    try:
        if data.hired == 0:
            print("true")
            data.hired = 1
            data.save()
        arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
            "Z", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '@', '#', '*', '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        raw_password = ""
        for i in range(10):
            raw_password = raw_password + random.choice(arr)
        # form = RegForm(email=data.mail,password=raw_password)
        # form.save()
        print("mailed")
        print("password "+ raw_password)
    except:
        pass
    return redirect("admin")


@login_required(login_url='/login/')
def admin_add(request):
    con = {
        "form": jobForm()
    }
    if request.POST:
        m = jobForm(request.POST)
        if m.is_valid():
            newForm = m.save(commit=False)
            newForm.creation_date = str(datetime.datetime.now())
            newForm.save()
        else:
            return render(request, "page/admin_profile.html", con)
    return render(request, "page/admin_profile.html", con)


@login_required(login_url='/login/')
def question_edit_home(request):
    con = {
        "data": Job.objects.all()
    }
    return render(request, "page/question-edit-home.html", con)

@login_required(login_url='/login/')
def question_edit_add(request, myid):
    if request.POST:
        data = adddata(request.POST)
        que = Job.objects.get(pk=myid)
        p = data.save(commit=False)
        p.jobid = que
        p.save()
    return render(request, "page/question-edit-add.html")

@login_required(login_url='/login/')
def question_edit_delete(request, myid):
    que = Job.objects.get(pk=myid)
    con = {
        "data": Mcq.objects.filter(jobid=que),
        "id": myid
        }
    return render(request, "page/question-edit-delete.html", con)

@login_required(login_url='/login/')
def question_edit_delete_main(request, myid, delid):
    obj = Mcq.objects.get(pk=delid)
    obj.delete()
    return redirect(question_edit_delete, myid)

@login_required(login_url='/login/')
def question_edit_update(request, myid):
    que = Job.objects.get(pk=myid)
    con = {
        "data": Mcq.objects.filter(jobid=que),
        "id": myid
        }
    return render(request, "page/question-edit-update.html", con)

@login_required(login_url='/login/')
def question_edit_update_main(request, myid, delid):
    if request.POST:
        obj = Mcq.objects.get(pk=delid)
        try:
            if request.POST["text"]:
                text = request.POST["text"]
                obj.question = text
                obj.save()
        except:
            pass
        try:
            if request.POST["answer"]:
                answer = request.POST["answer"]
                obj.answer = answer
                obj.save()
        except:
            pass
        try:
            if request.POST["option2"]:
                option2 = request.POST["option2"]
                obj.option2 = option2
                obj.save()
        except:
            pass
        try:
            if request.POST["option3"]:
                option3 = request.POST["option3"]
                obj.option3 = option3
                obj.save()
        except:
            pass

        try:
            if request.POST["option4"]:
                option4 = request.POST["option4"]
                obj.option4 = option4
                obj.save()
        except:
            pass
    return redirect(question_edit_update, myid)

def apply_job(request, myid):
    jobCheck = Job.objects.get(pk=myid)
    if request.POST:
        add = 0
        score = ""
        countData = Mcq.objects.filter(jobid=jobCheck).count()
        for i in Mcq.objects.all().filter(jobid=jobCheck):
            try:
                see = Mcq.objects.get(pk=i.id)
                if see.answer == request.POST[str(i.id)]:
                    add = add + 1
            except:
                pass

        if add == countData:
            form = Apply_form(request.POST, request.FILES)
            if form.is_valid():
                try:
                    post_added = form.save(commit=False)
                    post_added.jobid = jobCheck
                    post_added.apply_date = str(
                        datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                    post_added.score = add
                    post_added.save()
                except:
                    score = "Something Went WRONG"
            else:
                apply_job_data = {
                    "form": form,
                    "id": myid,
                }
                return render(request, "page/apply.html", apply_job_data)
        else:
            score = f"You are have scored {add} out of {countData}"
        return render(request, "page/apply.html", {"score": score})
    mcq = Mcq.objects.all().filter(jobid=jobCheck)
    data = []
    for i in mcq:
        arr = [i.answer, i.option2, i.option3, i.option4]
        random.shuffle(arr)
        if data == []:
            data = [{"question": i.question, "id": i.id, "other": arr}]
        else:
            data.append({"question": i.question, "id": i.id, "other": arr})
    apply_job_data = {
        "data": data,
        "form": Apply_form(),
        "id": myid,
    }
    return render(request, "page/apply.html", apply_job_data)


def apply_job_question(request, myid):
    jobCheck = Job.objects.get(pk=myid)
    apply_job_data = {
        "id": myid,
        "que": Mcq.objects.filter(jobid=jobCheck),
    }
    return render(request, "page/apply.html", apply_job_data)

def job_details(request, myid):
    job_details_data = {
        "id": myid,
        "data": Job.objects.get(pk=myid)
    }
    return render(request, "page/detail.html", job_details_data)
