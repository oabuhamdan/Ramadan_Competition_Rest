from django.contrib.auth.models import Permission
from django.core.validators import validate_comma_separated_integer_list, integer_validator
from django.db import models

from core.models import GeneralUser, Competition


# class PointFormat(models.Model):
#     id = models.CharField(max_length=64, default="", primary_key=True)
#     label = models.CharField(max_length=64, default="")
#     html = models.TextField(default="")


class Section(models.Model):
    label = models.CharField(default='', max_length=32)
    position = models.IntegerField(default=1)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_sections', null=True)

    def set_competition(self, competition):
        self.competition = competition

    def __str__(self):
        return self.label


class PointTemplate(models.Model):
    class FormType(models.TextChoices):
        Number = 'num', "Number"
        CheckBox = 'chk', "Check Box"
        Other = 'oth', "Other (Needs to be reviewed by the admin)"

    is_active = models.BooleanField(default=True)
    is_shown = models.BooleanField(default=True)
    order_in_section = models.IntegerField()
    custom_days = models.CharField(validators=[validate_comma_separated_integer_list], max_length=64, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="competition_point_templates", null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="competition_sections")

    label = models.CharField(max_length=128, default='')
    description = models.CharField(max_length=256, default='')
    form_type = models.CharField(max_length=3, choices=FormType.choices, default=FormType.Number)
    upper_units_bound = models.IntegerField(default=1)
    lower_units_bound = models.IntegerField(default=0)
    points_per_unit = models.IntegerField(default=1)

    class Meta:
        ordering = ('section__position', 'order_in_section')

    def set_competition(self, competition):
        self.competition = competition


#
# class ExtraChallengeTemplate(PointTemplate):
#     is_for_all = models.BooleanField(default=False)
#     is_temporary = models.BooleanField(default=False)
#     time_frame = models.DurationField(default=timedelta(days=1))
#     date_posted = models.DateTimeField(default=timezone.now)
#


class CompAdmin(GeneralUser):
    phone_number = models.CharField(max_length=15, validators=[integer_validator], default="0000000000")
    permissions = models.CharField(validators=[validate_comma_separated_integer_list], max_length=9,
                                   default="0,0,0,0,0")
    is_super_admin = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'competition_admins'


class CompGroup(models.Model):
    name = models.CharField(max_length=30, default='')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_groups', null=True)
    announcements = models.TextField(default="", blank=True)
    admin = models.ForeignKey(CompAdmin, on_delete=models.RESTRICT, related_name='managed_groups')

    def set_competition(self, competition):
        self.competition = competition

    def set_admin(self, admin):
        self.admin = admin
