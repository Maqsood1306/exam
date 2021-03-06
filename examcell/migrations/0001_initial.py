# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 19:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dept',
            fields=[
                ('dname', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='hallticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seatno', models.IntegerField()),
                ('hsem', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='nc_student',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('s_fname', models.CharField(max_length=15)),
                ('s_mname', models.CharField(max_length=15)),
                ('s_lname', models.CharField(max_length=15)),
                ('s_image', models.ImageField(upload_to='')),
                ('s_email', models.EmailField(max_length=100)),
                ('s_password', models.CharField(max_length=25)),
                ('s_address', models.CharField(max_length=200)),
                ('s_contact', models.IntegerField()),
                ('s_gender', models.CharField(max_length=7)),
                ('s_semno', models.IntegerField(default=1)),
                ('s_confirm', models.IntegerField(default=0)),
                ('sem1', models.IntegerField(default=0)),
                ('sem2', models.IntegerField(default=0)),
                ('sem3', models.IntegerField(default=0)),
                ('sem4', models.IntegerField(default=0)),
                ('sem5', models.IntegerField(default=0)),
                ('sem6', models.IntegerField(default=0)),
                ('sem7', models.IntegerField(default=0)),
                ('sem8', models.IntegerField(default=0)),
                ('dname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.dept')),
            ],
        ),
        migrations.CreateModel(
            name='notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.TextField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('time', models.DateTimeField(default=datetime.datetime(2017, 5, 5, 19, 12, 14, 494814, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test1m', models.IntegerField(default=0)),
                ('test2m', models.IntegerField(default=0)),
                ('testavg', models.IntegerField(default=0)),
                ('semm', models.IntegerField(default=0)),
                ('twm', models.IntegerField(default=0)),
                ('oralm', models.IntegerField(default=0)),
                ('totalm', models.IntegerField(default=0)),
                ('r_semno', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='reval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.result')),
            ],
        ),
        migrations.CreateModel(
            name='stud_id',
            fields=[
                ('studid', models.IntegerField(primary_key=True, serialize=False)),
                ('studname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('s_fname', models.CharField(max_length=15)),
                ('s_mname', models.CharField(max_length=15)),
                ('s_lname', models.CharField(max_length=15)),
                ('s_image', models.ImageField(upload_to='')),
                ('s_email', models.EmailField(max_length=100)),
                ('s_password', models.CharField(max_length=25)),
                ('s_address', models.CharField(max_length=200)),
                ('s_contact', models.IntegerField()),
                ('s_gender', models.CharField(max_length=7)),
                ('s_semno', models.IntegerField(default=1)),
                ('sem1', models.IntegerField(default=0)),
                ('sem2', models.IntegerField(default=0)),
                ('sem3', models.IntegerField(default=0)),
                ('sem4', models.IntegerField(default=0)),
                ('sem5', models.IntegerField(default=0)),
                ('sem6', models.IntegerField(default=0)),
                ('sem7', models.IntegerField(default=0)),
                ('sem8', models.IntegerField(default=0)),
                ('dname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.dept')),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('sb_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('sb_name', models.CharField(max_length=40)),
                ('test1', models.IntegerField()),
                ('test2', models.IntegerField()),
                ('sem', models.IntegerField()),
                ('tw', models.IntegerField()),
                ('oral', models.IntegerField()),
                ('theory_credit', models.IntegerField()),
                ('tw_prc_credit', models.IntegerField()),
                ('sem_no', models.IntegerField()),
                ('dname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.dept')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='sb_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.subject'),
        ),
        migrations.AddField(
            model_name='result',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.student'),
        ),
        migrations.AddField(
            model_name='photo',
            name='res',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.result'),
        ),
        migrations.AddField(
            model_name='hallticket',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examcell.student'),
        ),
    ]
