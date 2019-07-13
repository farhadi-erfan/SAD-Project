from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import Requester, User, Contributor
from core.models import RequesterProject, Project, SubProject, ContributorSubProject
from . import forms


@login_required
def project_creation_view(request):
    if request.POST:
        form = forms.ProjectCreationForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            RequesterProject.objects.create(
                project=obj, requester=Requester.objects.get(user=request.user))
            for i in range(obj.subprojects_num):
                SubProject.objects.create(
                    project=obj, percent=0)
            return redirect(reverse('core:home'))
        else:
            return render(request, 'core/create_project.html', {'form': form})
    else:
        form = forms.ProjectCreationForm()
        return render(request, 'core/create_project.html', {'form': form})


@login_required
def home(request):
    def get_user_projects(user):
        # import datetime
        # lipsum = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
        # return [{'name': 'ali', 'value': 10, 'description': lipsum, 'deadline': datetime.date.today}, {'name': 'bali', 'value': 30, 'description': lipsum, 'deadline': datetime.date.today}, {'name': 'vali', 'value': 40, 'description': lipsum, 'deadline': datetime.date.today}]
        # ps = RequesterProject.objects.filter(
        #     requester=Requester.objects.get(user=user)
        # ).values_list('project')

        ps = Project.objects.filter(
            requesterproject__requester=Requester.objects.get(user=user)
        )

        return ps

    def get_available_projects(user):
        psp = Project.objects.all()
        sps = SubProject.objects.all()
        csps = ContributorSubProject.objects.all()
        ps = []
        for p in psp:
            bad_p = False
            for sp in sps:
                if sp.project == p:
                    for csp in csps:
                        if sp == csp.sub_project and user == csp.contributor and not csp.done:
                            bad_p = True
                            break
            if not bad_p:
                ps += [p]
                # TODO - has to filter done projects
        return ps

    user = request.user
    if user.is_requester:
        projects = get_user_projects(user)
        return render(request, 'core/home.html', {'projects': projects, 'is_requester': True})
    else:
        projects = get_available_projects(user)
        return render(request, 'core/home.html', {'projects': projects, 'is_requester': False})


def credit(request):
    if request.POST:
        form = forms.ChargeCreditForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['charge_amount']
            request.user.credit += amount
            request.user.save()
        return render(request, 'billing/credit.html', {
            'success': True
        })
    else:
        form = forms.ChargeCreditForm()
        return render(request, 'billing/credit.html', {'form': form})


def withdraw(request):
    if request.POST:
        form = forms.WithdrawForm(request.POST)
        if form.is_valid():
            print('aaaaaaaa')
            request.user.credit = 0
            request.user.save()
            return render(request, 'billing/withdraw.html', {
                'success': True
            })
        else:
            return render(request, 'billing/withdraw.html', {
                'success': False
            })
    else:
        form = forms.WithdrawForm()
        return render(request, 'billing/withdraw.html', {
            'form': form,
            'amount': request.user.credit
        })


@login_required
def accept_task(request, project_id):
    prj = Project.objects.get(id=project_id)
    try:
        contributor = Contributor.objects.get(user=request.user)
        subprojects = SubProject.objects.filter(project=prj)
        for x in subprojects:
            if x and not x.done and not x.assigned:
                subproject = x
                break
    except Contributor.DoesNotExist:
        raise Http404
    except SubProject.DoesNotExist:
        raise Http404

    ContributorSubProject.objects.create(
        sub_project=subproject,
        contributor=contributor
    )
    subproject.assigned = True
    subproject.save()
    prj.subprojects_num -= 1
    prj.save()
    print('id:', subproject.id)
    return redirect(reverse('core:work', kwargs={'subproject_id': subproject.id}))


@login_required
def work(request, subproject_id):
    subproject = SubProject.objects.get(id=subproject_id)
    project = Project.objects.get(id=subproject.project.id)
    contributor = Contributor.objects.get(user=request.user)
    if request.POST:
        form = forms.ContributorSubProjectForm(request.POST, request.FILES)
        print("well: ")
        if form.is_valid():
            print("success")
            attachment = form.cleaned_data['attachment']
            for x in ContributorSubProject.objects.all():
                print('folan', str(x.contributor), str(x.sub_project))
            csp = ContributorSubProject.objects.get(
                sub_project=subproject,
                contributor=contributor
            )
            csp.attachment = attachment
            csp.save()
            subproject.done = True
            subproject.save()

            return redirect(reverse('core:home'))
        else:
            return render(request, 'core/submit_work.html',
                          {'form': forms.ContributorSubProjectForm, 'project': project, 'subproject':subproject})
    else:
        form = forms.ContributorSubProjectForm()
        return render(request, 'core/submit_work.html', {'form': form, 'project': project, 'subproject':subproject})
