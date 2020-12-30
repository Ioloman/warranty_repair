# Generated by Django 3.1.4 on 2020-12-24 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('passport_data', models.IntegerField()),
                ('pk_client', models.AutoField(db_column='PK_client', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'client',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('last_name', models.CharField(max_length=50)),
                ('pk_consultant', models.AutoField(db_column='PK_consultant', primary_key=True, serialize=False)),
                ('middle_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('consultant_number', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'consultant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('pk_expert', models.AutoField(db_column='PK_expert', primary_key=True, serialize=False)),
                ('expert_number', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'expert',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpertReport',
            fields=[
                ('pk_expert_report', models.AutoField(db_column='PK_expert_report', primary_key=True, serialize=False)),
                ('report_date', models.DateField()),
                ('problem_description', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'expert_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FixingDocument',
            fields=[
                ('document_date', models.DateField()),
                ('pk_fixing_document', models.AutoField(db_column='PK_fixing_document', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'fixing_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FixingReport',
            fields=[
                ('pk_fixing_report', models.AutoField(db_column='PK_fixing_report', primary_key=True, serialize=False)),
                ('report_date', models.DateField()),
            ],
            options={
                'db_table': 'fixing_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('pk_master', models.AutoField(db_column='PK_master', primary_key=True, serialize=False)),
                ('master_number', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PartReport',
            fields=[
                ('pk_part_report', models.AutoField(db_column='PK_part_report', primary_key=True, serialize=False)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'part_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_name', models.CharField(max_length=30)),
                ('pk_product', models.AutoField(db_column='PK_product', primary_key=True, serialize=False)),
                ('vendor_code', models.CharField(max_length=15)),
                ('warranty_start_date', models.DateField()),
                ('problem_description', models.CharField(blank=True, max_length=150, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('product_status', models.CharField(max_length=50)),
                ('manufacture_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductAcceptanceDocument',
            fields=[
                ('pk_acceptance', models.AutoField(db_column='PK_acceptance', primary_key=True, serialize=False)),
                ('document_date', models.DateField()),
                ('product_description', models.CharField(blank=True, max_length=150, null=True)),
                ('product_state_description', models.CharField(blank=True, max_length=150, null=True)),
                ('product_sale_date', models.DateField(blank=True, null=True)),
                ('problem_description', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'product_acceptance_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductReturnDocument',
            fields=[
                ('document_date', models.DateField()),
                ('product_state_description', models.CharField(blank=True, max_length=150, null=True)),
                ('pk_product_return_document', models.IntegerField(db_column='PK_product_return_document', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'product_return_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('detail_name', models.CharField(max_length=30)),
                ('vendor_code', models.CharField(max_length=15)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('pk_spare_part', models.AutoField(db_column='PK_spare_part', primary_key=True, serialize=False)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'spare_part',
                'managed': False,
            },
        ),
    ]