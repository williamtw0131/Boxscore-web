from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Boxscore(models.Model):
    user = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    opponent = models.CharField(max_length=30)
    player = models.PositiveSmallIntegerField()
    fgm = models.PositiveSmallIntegerField(default=0)
    fga = models.PositiveSmallIntegerField(default=0)
    threepm = models.PositiveSmallIntegerField(default=0)
    threepa = models.PositiveSmallIntegerField(default=0)
    ftm = models.PositiveSmallIntegerField(default=0)
    fta = models.PositiveSmallIntegerField(default=0)
    oreb = models.PositiveSmallIntegerField(default=0)
    dreb = models.PositiveSmallIntegerField(default=0)
    ast = models.PositiveSmallIntegerField(default=0)
    stl = models.PositiveSmallIntegerField(default=0)
    blk = models.PositiveSmallIntegerField(default=0)
    tov = models.PositiveSmallIntegerField(default=0)
    pf = models.PositiveSmallIntegerField(default=0)

    @property
    def fgave(self):
        if self.fgm <= self.fga:
            if self.fga == 0:
                fgave = "0"
            else:
                fgave = self.fgm / self.fga * 100
                fgave = "%.1f" % fgave
            return fgave + "%"

    @property
    def threepave(self):
        if self.threepm <= self.threepa:
            if self.threepa == 0:
                threepave = "0"
            else:
                threepave = self.threepm / self.threepa * 100
                threepave = "%.1f" % threepave
            return threepave + "%"

    @property
    def ftave(self):
        if self.ftm <= self.fta:
            if self.fta == 0:
                ftave = "0"
            else:
                ftave = self.ftm / self.fta * 100
                ftave = "%.1f" % ftave
            return ftave + "%"

    @property
    def reb(self):
        return self.oreb + self.dreb

    @property
    def pts(self):
        if self.fgm <= self.fga and self.threepm <= self.threepa and self.ftm <= self.fta:
            return self.fgm * 2 + self.threepm * 3 + self.ftm

    def submit(self):
        self.save()

    def __str__(self):
        return self.team_name
