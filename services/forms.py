from django.forms import ModelForm, DateField, SelectDateWidget, ModelChoiceField, Form
from .models import (Client, Product, SparePart, ExpertReport, FixingReport, ProductReturnDocument,
                     FixingDocument, ProductAcceptanceDocument)
from datetime import datetime


class ClientForm(ModelForm):
    START_DATE = 1900
    birthday = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата рождения'
    )

    class Meta:
        model = Client
        fields = ['first_name', 'middle_name', 'last_name', 'birthday', 'email', 'phone_number', 'passport_data']
        labels = {'first_name': 'Имя',
                  'middle_name': 'Отчество',
                  'last_name': 'Фамилия',
                  'birthday': 'Дата рождения',
                  'email': 'Эл. почта',
                  'phone_number': 'Тел. номер',
                  'passport_data': 'Пасспортные данные'}


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'problem_description', 'location', 'product_status']
        labels = {'product_name': 'Название',
                  'problem_description': 'Описание проблемы',
                  'location': 'Местонахождение',
                  'product_status': 'Статус'}


class NewProductForm(ModelForm):
    START_DATE = 2000
    warranty_start_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата начала гарантии'
    )

    class Meta:
        model = Product
        fields = ['product_name', 'problem_description', 'location', 'product_status',
                  'vendor_code', 'warranty_start_date', 'manufacture_number']
        labels = {'product_name': 'Название',
                  'problem_description': 'Описание проблемы',
                  'location': 'Местонахождение',
                  'product_status': 'Статус',
                  'vendor_code': 'Артикул',
                  'warranty_start_date': 'Дата начала гарантии',
                  'manufacture_number': 'Заводской номер'}


class SparePartForm(ModelForm):
    class Meta:
        model = SparePart
        fields = ['detail_name', 'vendor_code', 'price', 'amount']
        labels = {'detail_name': 'Название',
                  'vendor_code': 'Артикул',
                  'price': 'Цена за шт.',
                  'amount': 'Количество'}


class ExpertReportForm(ModelForm):
    START_DATE = 2000
    report_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата Отчета',
        initial=datetime.today()
    )

    class Meta:
        model = ExpertReport
        fields = ['problem_description', 'report_date']
        labels = {'problem_description': 'Описание проблемы',
                  'report_date': 'Дата отчета'}


class FixingDocumentForm(ModelForm):
    START_DATE = 2000
    document_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата заявления',
        initial=datetime.today()
    )

    class Meta:
        model = FixingDocument
        fields = ['document_date']
        labels = {'document_date': 'Дата заявления'}


class FixingReportForm(ModelForm):
    START_DATE = 2000
    report_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата отчета',
        initial=datetime.today()
    )

    class Meta:
        model = FixingReport
        fields = ['report_date']
        labels = {'report_date': 'Дата отчета'}


class AcceptanceDocumentForm(ModelForm):
    START_DATE = 2000
    document_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата акта',
        initial=datetime.today()
    )
    pk_client = ModelChoiceField(queryset=Client.objects.all(), empty_label=None, label='Клиент')

    class Meta:
        model = ProductAcceptanceDocument

        fields = ['document_date', 'product_description', 'product_state_description', 'problem_description', 'pk_client']
        labels = {'document_date': 'Дата акта',
                  'product_description': 'Описание продукта',
                  'product_state_description': 'Описание состояния',
                  'problem_description': 'Описание проблемы',
                  'pk_client': 'Клиент'}


class ReturnDocumentForm(ModelForm):
    START_DATE = 2000
    document_date = DateField(
        widget=SelectDateWidget(years=[i for i in range(START_DATE, int(datetime.today().year) + 1)]),
        label='Дата акта',
        initial=datetime.today()
    )

    class Meta:
        model = ProductReturnDocument
        fields = ['document_date', 'product_state_description']
        labels = {'document_date': 'Дата акта',
                  'product_state_description': 'Описание состояния'}


class ChoosePartForm(Form):
    part = ModelChoiceField(queryset=SparePart.objects.filter(amount__gt=0), label='Деталь')