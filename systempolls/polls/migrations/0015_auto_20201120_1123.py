# Generated by Django 2.2.10 on 2020-11-20 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20201119_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multichoiceanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_answers', to='polls.Question'),
        ),
    ]
