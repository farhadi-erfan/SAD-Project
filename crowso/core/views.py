import os

from io import BytesIO
import zipfile

from django.contrib import messages
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
            requester = Requester.objects.get(user=request.user)
            obj = form.save(commit=False)
            if obj.value > requester.user.credit:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'مبلغ پیشنهادی بیشتر از اعتبار حساب است.'
                )
                return redirect(reverse('core:create_project'))
            else:
                requester.user.credit -= obj.value
                print(requester.user.credit, obj.value)
                requester.save()
                requester.user.save()
            obj.save()
            RequesterProject.objects.create(
                project=obj, requester=requester)
            for i in range(obj.subprojects_num):
                SubProject.objects.create(
                    project=obj,
                    percent=0,
                    number=i,
                    price=obj.value / obj.subprojects_num,
                )
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

    def get_available_projects(self, user, query):
        psp = Project.objects.all()
        if query != "" and query is not None:
            psp = psp.filter(name__icontains=query)
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
            return self.handle_requester_home(request)
        else:
            return self.handle_contributor_home(request)

    def handle_requester_home(self, request):
        user = request.user
        requester = Requester.objects.get(user=user)
        projects = self.get_user_projects(user)
        print(projects)
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
        name_contains = request.GET.get('name_contains')
        user = request.user
        contributor = Contributor.objects.get(
            user=user
        )
        projects = self.get_available_projects(user, name_contains)
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
            messages.add_message(
                request,
                messages.SUCCESS,
                'با موفقیت پرداخت شد.'
            )
            return redirect(reverse('core:home'))
        else:
            messages.add_message(
                request,
                messages.MessageFailure,
                'پرداخت ناموفق!'
            )
            return render(request, 'billing/withdraw.html', {
                'success': False
            })
    else:
        form = forms.WithdrawForm()
        return render(request, 'billing/withdraw.html', {
            'form': form,
            'user': request.user
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
    template = 'core/project_view.html'
    try:
        project = Project.objects.get(
            id=project_id
        )
    except Project.DoesNotExist:
        raise Http404

    subprojects = SubProject.objects.filter(
        project=project
    )
    for sp in subprojects:
        if sp.assigned:
            csp = ContributorSubProject.objects.get(sub_project=sp)
            sp.attachment = csp.attachment
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
        SubProject.objects.create(
            project=subproject.project,
            number=subproject.number,
            percent=0,
            price=subproject.price
        )
    return redirect('core:home')


@login_required
def accept_subproject(request, sp_id):
    try:
        subproject = SubProject.objects.get(id=sp_id)
    except SubProject.DoesNotExist:
        raise Http404
    with transaction.atomic():
        subproject.accepted = True
        csp = ContributorSubProject.objects.get(
            sub_project=subproject
        )
        user = csp.contributor.user
        user.credit += subproject.price
        user.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        'تسک با موفقیت قبول شد!'
    )
    return redirect('core:home')


@login_required
def download_all_exports(request, project_id):
    project = Project.objects.get(id=project_id)

    filenames = []
    for sp in project.subproject_set.filter(done=True):
        if sp.assigned:
            csp = ContributorSubProject.objects.get(sub_project=sp)
            filenames += [csp.attachment.path]

    zip_subdir = "exportfiles"
    zip_filename = '{}.zip'.format(project.name)
    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")
    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%{}'.format(zip_filename)
    return resp
