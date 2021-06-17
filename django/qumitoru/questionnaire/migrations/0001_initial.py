# Generated by Django 2.2.24 on 2021-06-16 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=40)),
                ('scale_patarn', models.IntegerField(default=5)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionnaire.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Questionare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionareScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.IntegerField(null=True)),
                ('q2', models.IntegerField(null=True)),
                ('q3', models.IntegerField(null=True)),
                ('q4', models.IntegerField(null=True)),
                ('q5', models.IntegerField(null=True)),
                ('q6', models.IntegerField(null=True)),
                ('q7', models.IntegerField(null=True)),
                ('q8', models.IntegerField(null=True)),
                ('q9', models.IntegerField(null=True)),
                ('day_of_week', models.IntegerField()),
                ('file_path', models.CharField(max_length=40)),
                ('take_at', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('questionare', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionnaire.Questionare')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionareQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionnaire.Question')),
                ('questionare', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionnaire.Questionare')),
            ],
        ),
        migrations.AddField(
            model_name='questionare',
            name='question',
            field=models.ManyToManyField(through='questionnaire.QuestionareQuestion', to='questionnaire.Question'),
        ),
        migrations.AddField(
            model_name='questionare',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]