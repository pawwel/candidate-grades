from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
#from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from organizer.models import Grade, Candidate


# Create your views here.

class CreateGrade(LoginRequiredMixin,generic.CreateView):
    fields = ('value','task','candidate')
    model = Grade
    template_name = 'organizer/add-mark.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)

# Model unique_together checks if a task has already been graded.
# Alternatively could be checked here by forms.ValidationError
        # task = form.cleaned_data['task']
        # if Grade.objects.filter(task=task):
        #     raise forms.ValidationError("This task is already graded.")

        self.object.recruiter = self.request.user
        self.object.save()
        return super().form_valid(form)


@login_required
def candidate_list(request):

    candidates = Candidate.objects.prefetch_related('candidate_grades').all()
    candidate_list = []

    for candidate in candidates:
        pk = candidate.id
        full_name = candidate.first_name + ' ' + candidate.last_name
        grades = []

        for candidate_grade in candidate.candidate_grades.all():
            grades.append(candidate_grade.value)

        if len(grades)>0:
            avg_grade = round(sum(grades)/len(grades),2)
        else:
            avg_grade = 0

        single_candidate_dict = {'pk':pk,'full_name':full_name,'avg-grade':avg_grade,'grades':grades}
        candidate_list.append(single_candidate_dict)

    candidates_dict = {'data':candidate_list}
    return JsonResponse(candidates_dict, safe=False)
