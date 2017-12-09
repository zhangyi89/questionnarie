from django.db import models

# Create your models here.


class UserInfo(models.Model):
    """
    员工表
    """
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    学生表
    """
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    cls = models.ForeignKey(to="ClassList")

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    """
    问卷表
    """
    title = models.CharField(max_length=48)
    cls = models.ForeignKey(to="ClassList")
    creator = models.ForeignKey(to="UserInfo")

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    问题表
    """
    caption = models.CharField(max_length=64)
    question_type = (
        (1, "打分"),
        (2, "单选"),
        (3, "评价"),
    )
    tp = models.IntegerField(choices=question_type)
    questionnaire = models.ForeignKey(to="Questionnaire", default=0)

    def __str__(self):
        return self.caption


class Option(models.Model):
    """
    单选题的选项
    """
    name = models.CharField(verbose_name="选项名称", max_length=32)
    score = models.IntegerField(verbose_name="对应的分值")
    qs = models.ForeignKey(to="Question")

    def __str__(self):
        return self.name


class Answer(models.Model):
    """
    回答
    """
    stu = models.ForeignKey(to="Student")
    question = models.ForeignKey(to="Question")
    option = models.ForeignKey(to="Option", null=True, blank=True)
    val = models.IntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.stu
