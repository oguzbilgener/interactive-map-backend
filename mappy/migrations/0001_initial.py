# Generated by Django 2.0.1 on 2018-01-18 22:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiplomaticRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Canonical name of the event')),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, help_text='Flavor text, Wikipedia, etc.')),
            ],
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('source', models.TextField(help_text='Citation for where you found this map. Guide: http://rmit.libguides.com/harvardvisual/maps.')),
                ('start_date', models.DateField(help_text='When this border takes effect.')),
                ('end_date', models.DateField(help_text='When this border ceases to exist.')),
                ('end_event', models.ForeignKey(blank=True, help_text="If this field is set, this event's date overwrites the end_date", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prior_borders', to='mappy.Event')),
                ('start_event', models.ForeignKey(blank=True, help_text="If this field is set, this event's date overwrites the start_date", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_borders', to='mappy.Event')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Canonical name -- each state should have only one.')),
                ('aliases', models.TextField(blank=True, help_text='CSV of alternative names this state may be known by.')),
                ('description', models.TextField(blank=True, help_text='Links, flavor text, etc.')),
                ('color', models.TextField(help_text='I expect this to be the most controversial field.')),
                ('successors', models.ManyToManyField(blank=True, help_text='Successor states', related_name='predecessors', to='mappy.State')),
            ],
        ),
        migrations.AddField(
            model_name='shape',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mappy.State'),
        ),
        migrations.AddField(
            model_name='event',
            name='states',
            field=models.ManyToManyField(help_text='State(s) affected by this event.', to='mappy.State'),
        ),
    ]