from django.db.models import Sum


def get_contributed_percent(project):
    sum_ = project.subproject_set.aggregate(percent=Sum('percent'))
    return sum_['percent_sum']


def get_done_percent(project):
    sub_projects = project.subproject_set.all()
    percent = 0
    for sp in sub_projects:
        if sp.revision.accepted:
            percent += sp.percent
    return percent


def get_rejected_percent(project):
    sub_projects = project.subproject_set.all()
    percent = 0
    for sp in sub_projects:
        if sp.revision.is_rejected():
            percent += sp.percent
    return percent
