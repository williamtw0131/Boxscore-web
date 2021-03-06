# Generated by Django 2.1.3 on 2018-12-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxscore', '0002_game_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lifetime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=30)),
                ('player', models.PositiveSmallIntegerField()),
                ('fgm', models.PositiveSmallIntegerField(default=0)),
                ('fga', models.PositiveSmallIntegerField(default=0)),
                ('threepm', models.PositiveSmallIntegerField(default=0)),
                ('threepa', models.PositiveSmallIntegerField(default=0)),
                ('ftm', models.PositiveSmallIntegerField(default=0)),
                ('fta', models.PositiveSmallIntegerField(default=0)),
                ('oreb', models.PositiveSmallIntegerField(default=0)),
                ('dreb', models.PositiveSmallIntegerField(default=0)),
                ('ast', models.PositiveSmallIntegerField(default=0)),
                ('stl', models.PositiveSmallIntegerField(default=0)),
                ('blk', models.PositiveSmallIntegerField(default=0)),
                ('tov', models.PositiveSmallIntegerField(default=0)),
                ('pf', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
