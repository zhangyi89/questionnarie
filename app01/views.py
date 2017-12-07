from django.shortcuts import render, redirect
from app01 import models
from app01 import forms
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
        student_list = i.cls.student_set.all()
    # 每个班级人数

    return render(request, "questionnaire.html", locals())


def questionnaire_add(request):
    questionnaire_form = forms.QuestionnarieForm()
    if request.method == "POST":
        questionnaire_form = forms.QuestionnarieForm(request.POST)
        if questionnaire_form.is_valid():
            title = questionnaire_form.cleaned_data['title']
            cls = questionnaire_form.cleaned_data['cls']
            creator = questionnaire_form.cleaned_data['creator']
            models.Questionnaire.objects.create(title=title, cls_id=cls, creator_id=creator)
            return  redirect("/questionnaire/")
    return render(request, "questionnaire_add.html", locals())


def question(request, nid):
    # 根据ID过滤问题对象
    def form_list():
        question_obj = models.Question.objects.filter(questionnaire_id=nid)
        for i in question_obj:
            form = forms.QuestionModelForm(instance=i)
            tmp = {"form": form, "obj": i, "option_class": "hide", "options": None}
            if i.tp == 2:
                tmp['option_class'] = " "

                def option_list(obj):
                    option_obj = models.Option.objects.filter(qs=obj)
                    for j in option_obj:
                        form_option = forms.OptionModelForm(instance=j)
                        yield {"form": form_option, "obj": j}
                tmp['options'] = option_list(i)
            yield tmp
    return render(request, "question.html", {'form_list': form_list()})


def question_edit(request, id):
    # 获取问题类型
    question_form = forms.QuestionForm()

    if request.method == "POST":
        # 获取问卷id， 问题captial， 选项
        print("========")
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            print("+++++++++")
            caption = question_form.cleaned_data['caption']
            tp = question_form.cleaned_data['tp']
            print(id, caption, tp)
            return redirect("/questionnaire/")

    return render(request, "question_edit.html", {"question_form": question_form})
