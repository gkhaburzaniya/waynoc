# Generated by Django 2.0 on 2017-12-04 05:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('score', models.IntegerField(editable=False, null=True)),
            ],
            options={
                'ordering': ['-score', 'name'],
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='attendees',
            field=models.ManyToManyField(related_name='movies_attended', to='movienite.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='picker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies_picked', to='movienite.Person'),
        ),
    ]
