# Generated by Django 4.1 on 2024-03-15 07:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('venue_name', models.CharField(max_length=512, null=True)),
                ('floor_number', models.IntegerField(blank=True, null=True)),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerStatus',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=1024, unique=True)),
                ('included_queues', models.JSONField(default=list)),
                ('excluded_queues', models.JSONField(default=list)),
                ('timeout', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('last_tick', models.DateTimeField(default=django.utils.timezone.now)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('stopped', models.DateTimeField(blank=True, null=True)),
                ('exit_code', models.IntegerField(blank=True, choices=[(0, 'Stopped'), (77, 'Terminated'), (99, 'Crashed')], null=True)),
                ('exit_log', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Worker Status',
                'verbose_name_plural': 'Workers Statuses',
            },
        ),
        migrations.CreateModel(
            name='TaskExec',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=1024)),
                ('args', picklefield.fields.PickledObjectField(blank=True, default=list, editable=False)),
                ('kwargs', picklefield.fields.PickledObjectField(blank=True, default=dict, editable=False)),
                ('retries', models.IntegerField(default=0, help_text='retries left, -1 means infinite')),
                ('retry_delay', models.IntegerField(default=0, help_text='Delay before next retry in seconds. Will double after each failure.')),
                ('due', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('SLEEPING', 'Sleeping'), ('QUEUED', 'Queued'), ('PROCESSING', 'Processing'), ('SUCCEEDED', 'Succeeded'), ('INTERRUPTED', 'Interrupted'), ('FAILED', 'Failed'), ('INVALID', 'Invalid')], default='QUEUED', max_length=32)),
                ('result', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('stdout', models.TextField(blank=True, default='')),
                ('stderr', models.TextField(blank=True, default='')),
                ('replaced_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='toosimpleq.taskexec')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='toosimpleq.workerstatus')),
            ],
            options={
                'verbose_name': 'Task Execution',
            },
        ),
        migrations.CreateModel(
            name='ScheduleExec',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024, unique=True)),
                ('last_due', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('ACTIVE', 'Active'), ('INVALID', 'Invalid')], default='ACTIVE', max_length=32)),
                ('last_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='toosimpleq.taskexec')),
            ],
            options={
                'verbose_name': 'Schedule Execution',
            },
        ),
        migrations.CreateModel(
            name='ParkingArea',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('parking_area_name', models.CharField(max_length=512)),
                ('total_no_of_spots', models.IntegerField()),
                ('no_of_spots_occupied', models.IntegerField()),
                ('last_updated', models.DateTimeField()),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('agent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='toosimpleq.agent')),
            ],
        ),
    ]
