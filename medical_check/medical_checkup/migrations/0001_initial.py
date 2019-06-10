# Generated by Django 2.2.2 on 2019-06-09 14:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalCheckUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('conducted_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('conducted_month', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('course', models.PositiveSmallIntegerField(choices=[(0, '35歳未満男女コース'), (1, '35歳以上男性非管理職コース'), (2, '35歳以上女性非管理職コース'), (3, '35歳以上男性管理職コース'), (4, '35歳以上女性管理職コース')])),
                ('is_reexamination', models.BooleanField(default=False)),
                ('location', models.TextField()),
                ('consultation_date', models.DateField()),
                ('need_reexamination', models.BooleanField(default=False)),
                ('judgement_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
            ],
            options={
                'db_table': 'medical_checkups',
                'unique_together': {('employee', 'target_year', 'conducted_year', 'conducted_month')},
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('bmi', models.FloatField()),
                ('percentage_of_body_fat', models.FloatField()),
                ('checkup_ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medical_checkup.MedicalCheckUp')),
            ],
            options={
                'db_table': 'results',
            },
        ),
    ]
