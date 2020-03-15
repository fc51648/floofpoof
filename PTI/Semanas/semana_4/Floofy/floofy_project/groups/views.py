from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject
from login.views import is_student, is_teacher
from django.views.generic import (
    DetailView, UpdateView
)

@login_required(login_url="/")
def list_subjects(request):
    return render(request, 'groups/sel-sub.html')

def Select_Subject(request,sub_id=None):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=sub_id)
        except:
            raise Http404
        context = {}
        context['subject'] = subject
        context['groups'] = Group.objects.filter(subject=subject)
        for group in context['groups']:
            if request.user in group.members.all():
                context['group'] = group
        if request.user.is_teacher:
            return render(request, 'groups/groups-sub.html', context)
        if request.user.is_student:
            for group in Group.objects.filter(subject=subject):
                if request.user in group.members.all():
                    return render(request, 'mygroup/mygroup.html', context)
            return render(request, 'groups/groups-join.html', context)

def create_group(request,sub_id=None):
    context = {}
    subject = Subject.objects.get(id=sub_id)
    context['subject'] = subject
    if request.method == "POST":
        newgroup = Group(subject=subject)
        newgroup.save()
        newgroup.members.add(request.user)
        newgroup.name = request.POST.get('group_name')
        newgroup.save()
        context['group'] = newgroup
        return render(request, 'mygroup/mygroup.html', context)
    else:
        return render(request, 'groups/groups-create.html', context)


def join_group(request,sub_id=None):
    try:
        subject = Subject.objects.get(id=sub_id)
    except:
        raise Http404
    context = {}
    context['subject'] = subject
    context['groups'] = Group.objects.filter(subject=subject)
    return Select_Subject(request,sub_id)

def Set_Rules(request,sub_id=None):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=sub_id)
        except:
            raise Http404
        context = {}
        context['subject'] = subject
        return render(request, 'groups/groups-rules.html', context)
    if request.method == "POST":
        sub = Subject.objects.get(id=sub_id)
        if request.POST.get('groups_max'):
            sub.groups_max = request.POST.get('groups_max')
        if request.POST.get('groups_deadline'):
            sub.groups_deadline = request.POST.get('groups_deadline')
        if request.POST.get('groups_on'):
            sub.groups_on = request.POST.get('groups_on')
        sub.save()
        context = {}
        context['subject'] = sub
        return render(request, 'groups/groups-rules.html', context)

        



class Set_Stages(DetailView):
    model = Subject
    template_name = 'groups/groups-sub.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] = User.objects.all()
        context['subjects'] = Subject.objects.all()
        return context