# Generated by Django 4.1.5 on 2023-02-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_alter_patients_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='careplan',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('start', models.DateField()),
                ('stop', models.DateField()),
                ('patient', models.UUIDField()),
                ('encounter', models.UUIDField()),
                ('code', models.CharField(max_length=8)),
                ('description', models.CharField(max_length=255)),
                ('reason_code', models.CharField(max_length=8)),
                ('reason_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('stop', models.DateField(blank=True, null=True)),
                ('patient', models.UUIDField()),
                ('encounter', models.UUIDField()),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField(blank=True, null=True)),
                ('patient', models.UUIDField()),
                ('encounter', models.UUIDField()),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('udi', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='encounter',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('patient', models.UUIDField()),
                ('organization', models.UUIDField()),
                ('provider', models.UUIDField()),
                ('payer', models.UUIDField()),
                ('encounter_class', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('base_encounter_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_claim_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payer_coverage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reason_code', models.CharField(blank=True, max_length=20, null=True)),
                ('reason_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='imaging_studies',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('patient', models.UUIDField()),
                ('encounter', models.UUIDField()),
                ('body_site_code', models.PositiveIntegerField()),
                ('body_site_description', models.CharField(max_length=255)),
                ('modality_code', models.CharField(max_length=255)),
                ('modality_description', models.CharField(max_length=255)),
                ('sop_code', models.CharField(max_length=255)),
                ('sop_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='immunization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('patient', models.CharField(max_length=36)),
                ('encounter', models.CharField(max_length=36)),
                ('code', models.PositiveSmallIntegerField()),
                ('description', models.CharField(max_length=100)),
                ('base_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='observations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('patient', models.CharField(max_length=36)),
                ('encounter', models.CharField(max_length=36)),
                ('code', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('units', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='organizations',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('phone', models.CharField(max_length=15)),
                ('revenue', models.FloatField()),
                ('utilization', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='payer_transitions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.CharField(max_length=36)),
                ('start_year', models.PositiveSmallIntegerField()),
                ('end_year', models.PositiveSmallIntegerField()),
                ('payer', models.CharField(max_length=36)),
                ('ownership', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='payers',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state_headquartered', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('amount_covered', models.FloatField()),
                ('amount_uncovered', models.FloatField()),
                ('revenue', models.FloatField()),
                ('covered_encounters', models.PositiveIntegerField()),
                ('uncovered_encounters', models.PositiveIntegerField()),
                ('covered_medications', models.PositiveIntegerField()),
                ('uncovered_medications', models.PositiveIntegerField()),
                ('covered_procedures', models.PositiveIntegerField()),
                ('uncovered_procedures', models.PositiveIntegerField()),
                ('covered_immunizations', models.PositiveIntegerField()),
                ('uncovered_immunizations', models.PositiveIntegerField()),
                ('unique_customers', models.PositiveIntegerField()),
                ('qols_avg', models.FloatField()),
                ('member_months', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('patient', models.CharField(max_length=36)),
                ('encounter', models.CharField(max_length=36)),
                ('code', models.CharField(max_length=36)),
                ('description', models.CharField(max_length=255)),
                ('base_cost', models.FloatField()),
                ('reasoncode', models.CharField(blank=True, max_length=36, null=True)),
                ('reasondescription', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='provider',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('organization', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('speciality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=10)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('utilization', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='supplies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('patient', models.CharField(max_length=36)),
                ('encounter', models.CharField(max_length=36)),
                ('code', models.CharField(max_length=36)),
                ('description', models.TextField()),
                ('quantity', models.FloatField()),
            ],
        ),
    ]