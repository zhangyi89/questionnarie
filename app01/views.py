import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.validators import  ValidationError
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from app01 import models
from app01 import forms


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        stu_obj = models.Student.objects.filter(name=username, pwd=pwd)
        if stu_obj:
            request.session['student_info'] = {"id": stu_obj[0].id, "username": username, "class_id": stu_obj[0].cls.id}
            return redirect("/answer/" + str(stu_obj[0].cls.id) + "/")
        user_obj = models.UserInfo.objects.filter(name=username, pwd=pwd)
        if user_obj:
            request.session['user_info'] = {"id": user_obj[0].id, "username": username}
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
            return redirect("/questionnaire/")
    return render(request, "questionnaire_add.html", locals())


def question(request, nid):
    # 根据ID过滤问题对象
    def form_list():
        question_obj = models.Question.objects.filter(questionnaire_id=nid)
        if not question_obj:
            form = forms.QuestionModelForm()
            form_option = forms.OptionModelForm()
            yield {"form": form, "obj": None, "option_class": "hide", "options": None}
        else:
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

    if request.method == "POST":
        ret = {'status': True, 'msg': None, 'data': None}
        try:
            # 取到前端提交的数据
            data = json.loads(request.body.decode("utf8"))
            # 获取当前问卷的问题列表
            question_list = models.Question.objects.filter(questionnaire_id=nid)
            # 当前问题列表ID和提交的问题列表ID做对比，求出qid_list里有的，did_list没有的，并在数据库中删除这些ID的内容
            qid_list = [i.id for i in question_list]
            did_list = [int(i.get("id")) for i in data if i.get("id")]
            del_id_list = set(qid_list).difference(did_list)
            # 添加或更新用户提交的每个问题
            for item in data:
                qid = item.get("id")
                print(qid)
                caption = item.get("caption")
                tp = int(item.get("tp"))
                options = item.get("options")
                # 新增的问题
                if not item.get("id"):
                    print("not in qid_list")
                    question_obj = models.Question.objects.create(caption=caption, tp=tp, questionnaire_id=nid)
                    # 如果有选项
                    print(tp,type(tp))
                    if tp == 2:
                        for op in options:
                            print("==========================")
                            print(op.get("name"), op.get("score"))
                            options_obj = models.Option.objects.create(name=op.get("name"), score=op.get("score"),
                                                                       qs=question_obj)
                # 更新的问题
                else:
                    print("in qid_list")
                    models.Question.objects.filter(id=qid).update(caption=caption, tp=tp)
                    # 判断更新的问题有没有选项
                    if not options:
                        models.Option.objects.filter(qs_id=qid).delete()
                    # 如果有选项（应该把提交的选项和数据库中的选项做对比，判断选项的更新、添加还是删除
                    else:
                        # 不推荐的做法（直接删除数据库中的选项，添加用户提交的选项）
                        models.Option.objects.filter(qs_id=qid).delete()
                        for op in options:
                            models.Option.objects.create(name=op.get("name"), score=op.get("score"), qs_id=qid)
            models.Question.objects.filter(id__in=del_id_list).delete()
        except Exception as e:
            ret['status'] = False
            ret['msg'] = str(e)
        return JsonResponse(ret)
    return render(request, "question.html", {'form_list': form_list()})


def answer_list(request, class_id):
    if request.session.get("student_info") and request.session.get("student_info").get("class_id") == int(class_id):
        # 获取该班级所有的问卷
        questionnaire_list = models.Questionnaire.objects.filter(cls_id=int(class_id))
        class_name = models.ClassList.objects.get(id=int(class_id)).title
        return render(request, "answer_list.html", {"questionnaire_list": questionnaire_list, "class_name":class_name})

    return redirect("/login/")


def func(val):
    if len(val) < 15:
        raise ValidationError("最少输入15字符！")


def answer_detail(request,class_id, qid):
    student_id = request.session['student_info']['id']
    # 查看是否是当前问卷班级的学生
    class_check = models.Student.objects.filter(id=student_id, cls_id=class_id).count()
    if not class_check:
        return redirect("/login/")
    # 检查该用户是否提交过
    submit_check = models.Answer.objects.filter(stu_id=student_id, question__questionnaire_id=qid).count()
    if submit_check:
        return HttpResponse("你已经提交过了！")
    # 展示当前问卷的内容
    # 获取当前问卷的问题列表
    question_list = models.Question.objects.filter(questionnaire_id=qid)
    question_dict = {}
    for item in question_list:
        # 分别取出不同类型的问题
        if item.tp == 1:
            question_dict['val_%s' % item.id] = fields.ChoiceField(
                label=item.caption,
                error_messages={"required": "不能为空"},
                widget=widgets.RadioSelect,
                choices=[(i, i) for i in range(1, 11)]
            )
        elif item.tp == 2:
            question_dict['option_id_%s' % item.id] = fields.ChoiceField(
                label=item.caption,
                error_messages={"required": "不能为空"},
                widget=widgets.RadioSelect,
                choices=models.Option.objects.filter(qs_id=item.id).values_list("id", "name")
            )
        else:
            question_dict['content_%s' % item.id] = fields.CharField(
                label=item.caption,
                error_messages={"required":"不能为空"},
                widget=widgets.Textarea,
                # 调用func函数用来验证
                validators=([func, ])
            )
    # 通过type创建Form类，,可以循环的创建数据,question_dict为字段
    question_list_form = type("question_list_form", (Form,), question_dict)

    # 当get请求是，获取form对象，生成选项框
    if request.method == "GET":
        form = question_list_form()
        return render(request, "answer_detail.html", {"question_list": question_list, "form": form})
    else:
        # 验证用户提交的数据
        form = question_list_form(request.POST)
        answer_obj = []
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                print(form.cleaned_data)
                t, qid = k.rsplit("_", 1)
                answer_dict = {"stu_id": student_id, "question_id": qid, t: v}
                answer_obj.append(models.Answer(**answer_dict))
            models.Answer.objects.bulk_create(answer_obj)
            return HttpResponse("感谢您的参与！")
        return render(request, "answer_detail.html", {"question_list": question_list, "form": form})


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
