# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revision',
            name='parent_revision',
        ),
        migrations.AddField(
            model_name='revision',
            name='parent',
            field=models.ForeignKey(to='wiki.Revision', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
