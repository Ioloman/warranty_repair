# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class UserExtent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_extent = models.CharField(max_length=20)


class Client(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    passport_data = models.IntegerField()
    pk_client = models.AutoField(db_column='PK_client', primary_key=True)  # Field name made lowercase.

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} - {self.passport_data}'

    class Meta:
        managed = False
        db_table = 'client'


class Consultant(models.Model):
    last_name = models.CharField(max_length=50)
    pk_consultant = models.AutoField(db_column='PK_consultant', primary_key=True)  # Field name made lowercase.
    middle_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    birthday = models.DateField()
    consultant_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.consultant_number}'

    class Meta:
        managed = True
        db_table = 'consultant'


class Expert(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    birthday = models.DateField()
    pk_expert = models.AutoField(db_column='PK_expert', primary_key=True)  # Field name made lowercase.
    expert_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.expert_number}'

    class Meta:
        managed = True
        db_table = 'expert'


class ExpertReport(models.Model):
    pk_expert_report = models.AutoField(db_column='PK_expert_report', primary_key=True)  # Field name made lowercase.
    report_date = models.DateField()
    problem_description = models.CharField(max_length=150)
    pk_acceptance = models.ForeignKey('ProductAcceptanceDocument', models.DO_NOTHING, db_column='PK_acceptance')  # Field name made lowercase.
    pk_expert = models.ForeignKey(Expert, models.DO_NOTHING, db_column='PK_expert')  # Field name made lowercase.

    def __str__(self):
        return f"""Дата отчета: {self.report_date.strftime('%d.%m.%Y')}\n 
Описание проблемы: {self.problem_description}\n
Эксперт: {self.pk_expert}\n 
Товар: {self.pk_acceptance.pk_product}\n 
Клиент: {self.pk_acceptance.pk_client}"""

    class Meta:
        managed = False
        db_table = 'expert_report'
        unique_together = (('pk_expert_report', 'pk_acceptance'),)


class FixingDocument(models.Model):
    document_date = models.DateField()
    pk_fixing_document = models.AutoField(db_column='PK_fixing_document', primary_key=True)  # Field name made lowercase.
    pk_acceptance = models.ForeignKey('ProductAcceptanceDocument', models.DO_NOTHING, db_column='PK_acceptance')  # Field name made lowercase.

    def __str__(self):
        return f"""Дата отчета: {self.document_date.strftime('%d.%m.%Y')}\n
Товар: {self.pk_acceptance.pk_product}\n 
Клиент: {self.pk_acceptance.pk_client}\n
Консультант: {self.pk_acceptance.pk_consultant}"""

    class Meta:
        managed = False
        db_table = 'fixing_document'
        unique_together = (('pk_fixing_document', 'pk_acceptance'),)


class FixingReport(models.Model):
    pk_fixing_report = models.AutoField(db_column='PK_fixing_report', primary_key=True)  # Field name made lowercase.
    report_date = models.DateField()
    pk_acceptance = models.ForeignKey('ProductAcceptanceDocument', models.DO_NOTHING, db_column='PK_acceptance')  # Field name made lowercase.
    pk_master = models.ForeignKey('Master', models.DO_NOTHING, db_column='PK_master')  # Field name made lowercase.

    def __str__(self):
        string = f"""Дата отчета: {self.report_date.strftime('%d.%m.%Y')}\n
Товар: {self.pk_acceptance.pk_product}\n 
Клиент: {self.pk_acceptance.pk_client}\n
Мастер: {self.pk_master}"""
        part_reports = PartReport.objects.filter(pk_fixing_report=self.pk_fixing_report)
        spare_parts = [SparePart.objects.get(pk_spare_part=part.pk_spare_part.pk_spare_part) for part in part_reports]
        if spare_parts:
            string += '\n\nДетали: \n'
            for part in spare_parts:
                string += str(part)
                string += '\n'
        return string

    class Meta:
        managed = False
        db_table = 'fixing_report'
        unique_together = (('pk_fixing_report', 'pk_acceptance'),)


class Master(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    birthday = models.DateField()
    pk_master = models.AutoField(db_column='PK_master', primary_key=True)  # Field name made lowercase.
    master_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.master_number}'

    class Meta:
        managed = True
        db_table = 'master'


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    pk_product = models.AutoField(db_column='PK_product', primary_key=True)  # Field name made lowercase.
    vendor_code = models.CharField(max_length=15)
    warranty_start_date = models.DateField()
    problem_description = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    STATUS_CHOICES = [
        ('U', 'В использовании'),  # акт о принятии
        ('OC', 'У консультанта'),  # забрал эксперт
        ('WE', 'Ожидает экспертной оценки'),  # сделал экспертизу
        ('OE', 'У эксперта'),  # забрал консультант
        ('WC', 'Ожидает подтверждения на ремонт'),  # составили подтверждение
        ('OC2', 'У консультанта перед ремонтом'),  # забрал мастер
        ('WF', 'Ожидает ремонта'),  # сделал ремонт
        ('OM', 'У мастера'),  # забрал консультант
        ('WR', 'Ожидает возврата'),  # забрал клиент (составили док)
    ]
    product_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='U')
    manufacture_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.product_name} - артикул: {self.vendor_code} - заводской номер: {self.manufacture_number}'

    class Meta:
        managed = False
        db_table = 'product'


class ProductAcceptanceDocument(models.Model):
    pk_acceptance = models.AutoField(db_column='PK_acceptance', primary_key=True)  # Field name made lowercase.
    document_date = models.DateField()
    product_description = models.CharField(max_length=150, blank=True, null=True)
    product_state_description = models.CharField(max_length=150, blank=True, null=True)
    product_sale_date = models.DateField(blank=True, null=True)
    problem_description = models.CharField(max_length=150)
    pk_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='PK_client')  # Field name made lowercase.
    pk_consultant = models.ForeignKey(Consultant, models.DO_NOTHING, db_column='PK_consultant')  # Field name made lowercase.
    pk_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='PK_product')  # Field name made lowercase.

    def __str__(self):
        return f"""Дата отчета: {self.document_date.strftime('%d.%m.%Y')}\n
Клиент: {self.pk_client}\n
Товар: {self.pk_product}\n
Консультант: {self.pk_consultant}\n
Описание товара: {self.product_description}\n
Описание состояния товара: {self.product_state_description}\n
Дата продажи товара: {self.product_sale_date.strftime('%d.%m.%Y')}\n
Описание проблемы: {self.problem_description}"""

    class Meta:
        managed = False
        db_table = 'product_acceptance_document'


class ProductReturnDocument(models.Model):
    document_date = models.DateField()
    product_state_description = models.CharField(max_length=150, blank=True, null=True)
    pk_product_return_document = models.AutoField(db_column='PK_product_return_document', primary_key=True)  # Field name made lowercase.
    pk_consultant = models.ForeignKey(Consultant, models.DO_NOTHING, db_column='PK_consultant')  # Field name made lowercase.
    pk_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='PK_product')  # Field name made lowercase.

    def __str__(self):
        return f"""Дата отчета: {self.document_date.strftime('%d.%m.%Y')}\n
Товар: {self.pk_product}\n
Консультант: {self.pk_consultant}\n
Описание состояния товара: {self.product_state_description}"""

    class Meta:
        managed = False
        db_table = 'product_return_document'


class PartReport(models.Model):
    pk_fixing_report = models.ForeignKey(FixingReport, models.DO_NOTHING, db_column='PK_fixing_report')  # Field name made lowercase.
    pk_spare_part = models.ForeignKey('SparePart', models.DO_NOTHING, db_column='PK_spare_part')  # Field name made lowercase.
    # тут был FixingReport вместо ProductAcceptanceDocument
    pk_acceptance = models.ForeignKey(ProductAcceptanceDocument, models.DO_NOTHING, db_column='PK_acceptance', related_name='%(class)s_requests_created')  # Field name made lowercase.
    pk_part_report = models.AutoField(db_column='PK_part_report', primary_key=True)  # Field name made lowercase.
    price = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'part_report'


class SparePart(models.Model):
    detail_name = models.CharField(max_length=30)
    vendor_code = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    pk_spare_part = models.AutoField(db_column='PK_spare_part', primary_key=True)  # Field name made lowercase.
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.detail_name} - артикул:{self.vendor_code} - цена: {self.price}'

    class Meta:
        managed = False
        db_table = 'spare_part'
