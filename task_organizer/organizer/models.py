from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Changing default django admin.User __str__ display to firts & last name.
# Should be done w/ Custom admin model if deeper changes required.
def get_first_last_name(self):
    return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_first_last_name)



class Grade(models.Model):
# On_delete:    delete all grades when candidate deleted;
#               keep grades (w/empty recruiter) when recruited deleted

    value = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(10)])

# Use unique=True if a given task could be graded only one time
# (multiple candidates cannot conduct the same task)

# If multiple candidates are allowed to conduct the same task and be graded
# use unique_together = ['task','candidate'] in class Meta func.
# Need to remove unique=True from self.task too.

    task = models.ForeignKey('organizer.Task',related_name='task_grades',
                                        unique=True, on_delete=models.CASCADE)
    candidate = models.ForeignKey('organizer.Candidate',related_name='candidate_grades',
                                        on_delete=models.CASCADE)
    recruiter = models.ForeignKey(User,related_name='recruiter_grades',
                                        null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return '{} {}; task = "{}"; grade = "{}"'.format(self.candidate.first_name,
                                        self.candidate.last_name, self.task, self.value)

    def get_absolute_url(self):
        return reverse('home')

    class Meta():
        ordering = ['candidate']



class Candidate(models.Model):

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Task(models.Model):

    task = models.TextField()

    def __str__(self):
        return self.task[:100] + '...'
