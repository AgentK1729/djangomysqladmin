# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('real', models.IntegerField(max_length=3)),
                ('img', models.IntegerField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
