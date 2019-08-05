from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

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


class HomeView(View):
    template = 'core/home.html'

    def get_user_projects(self, user):
        ps = Project.objects.filter(
            requesterproject__requester=Requester.objects.get(user=user)
        )
        return ps

    def get_available_projects(self, user):
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

    @method_decorator([
        login_required
    ])
    def get(self, request):
        user = request.user
        if user.is_requester:
            self.handle_requester_home(request)
        else:
            self.handle_contributor_home(request)

    def handle_requester_home(self, request):
        user = request.user
        requester = Requester.objects.get(user=user)
        projects = self.get_user_projects(user)
        return render(request, self.template, {
            'projects': projects,
            'is_requester': True
        })

    def get_contributor_subprojects(self, contributor):
        csp = ContributorSubProject.objects.select_related('sub_project').filter(
            contributor=contributor
        ).values_list('sub_project_id', flat=True)
        subprojects = SubProject.objects.filter(
            id__in=csp
        ).order_by('contributor__deadline_date')
        return subprojects

    def handle_contributor_home(self, request):
        user = request.user
        contributor = Contributor.objects.get(
            user=user
        )
        projects = self.get_available_projects(user)
        subprojects = self.get_contributor_subprojects(contributor)
        return render(request, self.template, {
            'projects': projects,
            'is_requester': False,
            'accepted_sps': subprojects
        })


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
    accepted_subprojects_count = ContributorSubProject.objects.filter(
        contributor__user=request.user,
        sub_project__project=prj
    ).count()
    if accepted_subprojects_count > 0:
        raise Http404
    try:
        contributor = Contributor.objects.get(user=request.user)
        subprojects = SubProject.objects.filter(project=prj)
        subproject = None
        for x in subprojects:
            if x and not x.done and not x.assigned:
                subproject = x
                break

    except Contributor.DoesNotExist:
        raise Http404
    except SubProject.DoesNotExist:
        raise Http404
    if not subproject:
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


@login_required
def project_state_view(request, project_id):
    template = ''
    try:
        project = Project.objects.get(
            id=project_id
        )
    except Project.DoesNotExist:
        raise Http404

    subprojects = SubProject.objects.filter(
        project=project
    )
    return render(request, template, context={
        'subprojects': subprojects,
        'project': project
    })


@login_required
def deny_subproject(request, sp_id):
    try:
        subproject = SubProject.objects.get(id=sp_id)
    except SubProject.DoesNotExist:
        raise Http404
    with transaction.atomic():
        subproject.accepted = False
        subproject.save()
    return redirect('core:home')


@login_required
def accept_subproject(request, sp_id):
    try:
        subproject = SubProject.objects.get(id=sp_id)
    except SubProject.DoesNotExist:
        raise Http404
    with transaction.atomic():
        subproject.accepted = True
        user = subproject.contributor.contributor.user
        user.credit += subproject.price
        user.save()
    return redirect('core:home')