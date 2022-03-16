import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from Ramadan_Competition_Rest import settings
from compAdmin.models import PointTemplate, CompGroup
from core.models import GeneralUser


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    filename = f'{instance.competition.id}/{instance.username}.{extension}'
    if os.path.exists(settings.MEDIA_URL+filename):
        os.remove(settings.MEDIA_URL+filename)
    return filename


class StudentUser(GeneralUser):
    profile_photo = models.ImageField(upload_to=upload_location, blank=True)
    read_only = models.BooleanField(default=False)
    group = models.ForeignKey(CompGroup, on_delete=models.CASCADE, related_name='group_students', null=True)

    def set_competition(self, competition):
        self.competition = competition

    class Meta:
        default_related_name = 'competition_students'
        ordering = ('first_name', 'last_name')

    @property
    def total_points(self):
        total = self.student_points.aggregate(Sum('point_total'))['point_total__sum']
        return total if total else 0

    def total_points_on_day(self, ramadan_day):
        total = self.student_points.filter(ramadan_record_date=ramadan_day).values('student__first_name',
                                                                                   'student__last_name',
                                                                                   'ramadan_record_date').annotate(
            points_per_day=Sum('point_total'))
        return total


class PointRecord(models.Model):
    point_template = models.ForeignKey(PointTemplate, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, null=True, related_name='student_points')
    point_scored_units = models.IntegerField(default=1)
    details = models.TextField(default='')
    ramadan_record_date = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    point_total = models.IntegerField(default=1)

    def set_student(self, student):
        self.student = student

    def set_point_total(self, point_total):
        self.point_total = point_total

    class Meta:
        ordering = ('-ramadan_record_date',)
