from django.shortcuts import render, redirect
from app01 import models
# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        if models.UserInfo.objects.get(name=username, pwd=pwd):
            return redirect("/questionnaire/")

    return render(request, "login.html")


def questionnaire(request):
    # 获取问卷对象
    questionnaire_obj = models.Questionnaire.objects.all()
    for i in questionnaire_obj:
        class_obj = i.cls.title
        print(class_obj)
    return render(request, "questionnaire.html", locals())
