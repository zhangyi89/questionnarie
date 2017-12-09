"""questionnaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r"login/", views.login),
    url(r"questionnaire/", views.questionnaire, name="questionnaire"),
    url(r'^questionnaire_add/$', views.questionnaire_add, name="questionnaire_add"),
    url(r'^question/(?P<nid>\d+)$', views.question, name="question"),
    url(r'question_edit/(?P<id>\d+)$', views.question_edit),
    url(r'^answer/(?P<class_id>\d+)/$', views.answer_list, name="answer_list"),
    url(r'^answer/(?P<class_id>\d+)/(?P<qid>\d+)/$', views.answer_detail, name="answer_detail")

]
