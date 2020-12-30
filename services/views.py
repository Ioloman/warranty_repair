from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import (Product, Client, SparePart, ProductReturnDocument, Master, Consultant, Expert, PartReport,
                     ProductAcceptanceDocument, FixingDocument, FixingReport, ExpertReport, UserExtent)
from .forms import (ClientForm, ProductForm, NewProductForm, SparePartForm,
                    ReturnDocumentForm, AcceptanceDocumentForm, FixingDocumentForm,
                    FixingReportForm, ExpertReportForm, ChoosePartForm)
from .context_processor import data
from django.http import HttpResponseRedirect

# Create your views here.


def login_user(request):
    if request.method == 'GET':
        return render(request, '../templates/services/log_in.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, '../templates/services/log_in.html',
                          {'form': AuthenticationForm(), 'error': "Username and/or password didn't match"})
        else:
            login(request, user)
            return redirect('main:home')


@login_required
def home(request):
    if request.method == 'GET':
        dictionary = {}
        if data(request)['employee'] == 'consultant':
            dictionary = {'clients': Client.objects.all()}
        elif data(request)['employee'] == 'master':
            dictionary = {'details': SparePart.objects.all()}
        return render(request, '../templates/services/home.html', dictionary)
    elif request.method == 'POST':
        pass


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def redir(request):
    if request.method == 'GET':
        return redirect('main:home')


@login_required
def product_list(request):
    if request.method == 'GET':
        return render(request, '../templates/services/list.html')
    elif request.method == 'POST':
        return product(request, None)


@login_required
def product(request, product_pk):
    if product_pk:
        pr = Product.objects.get(pk_product=product_pk)
        if request.method == 'GET':
            pr = Product.objects.get(pk_product=product_pk)
            form = ProductForm(instance=pr)

            employee = data(request)['employee']
            employee_number = UserExtent.objects.get(user=request.user).user_extent
            acceptance = ProductAcceptanceDocument.objects.filter(pk_product=product_pk)
            if employee == 'consultant':
                consultant = Consultant.objects.get(consultant_number=employee_number)
                reports = []
                acceptance = acceptance.filter(pk_consultant=consultant.pk_consultant).order_by('-document_date')
                reports.extend(map(lambda x: (x, 'acceptance'), list(acceptance)))
                reports.extend(map(lambda x: (x, 'fixing_document'), list(FixingDocument.objects.filter(pk_acceptance__in=acceptance).order_by('-document_date'))))
                reports.extend(map(lambda x: (x, 'return'), list(ProductReturnDocument.objects.filter(pk_product=product_pk, pk_consultant=consultant.pk_consultant).order_by('-document_date'))))
            elif employee == 'master':
                master = Master.objects.get(master_number=employee_number)
                reports = FixingReport.objects.filter(pk_master=master.pk_master, pk_acceptance__in=acceptance).order_by('-report_date')
                reports = map(lambda x: (x, 'fixing_report'), reports)
            elif employee == 'expert':
                expert = Expert.objects.get(expert_number=employee_number)
                reports = ExpertReport.objects.filter(pk_expert=expert.pk_expert, pk_acceptance__in=acceptance).order_by('-report_date')
                reports = map(lambda x: (x, 'expert'), reports)
            return render(request, '../templates/services/product.html', {'product': pr, 'form': form, 'reports': reports})
        elif request.method == 'POST':
            if 'save-product' in request.POST:
                form = ProductForm(request.POST, instance=pr)
                form.save()
                return redirect('main:product_list')
            elif 'to-wc' in request.POST:
                pr.product_status = 'WC'
                pr.save()
                return HttpResponseRedirect(request.path_info)
            elif 'to-wr' in request.POST:
                pr.product_status = 'WR'
                pr.save()
                return HttpResponseRedirect(request.path_info)
            elif 'to-we' in request.POST:
                pr.product_status = 'WE'
                pr.save()
                return HttpResponseRedirect(request.path_info)
            elif 'to-wf' in request.POST:
                pr.product_status = 'WF'
                pr.save()
                return HttpResponseRedirect(request.path_info)
    else:
        if request.method == 'POST':
            if 'new-product' in request.POST:
                form = NewProductForm()
                return render(request, '../templates/services/product.html', {'form': form})
            elif 'save-product' in request.POST:
                form = NewProductForm(request.POST)
                form.save()
                return redirect('main:product_list')


@login_required
def client(request, client_pk):
    if client_pk:
        client_ = Client.objects.get(pk_client=client_pk)
        if request.method == 'GET':
            form = ClientForm(instance=client_)
            return render(request, '../templates/services/client.html', {'form': form})
        elif request.method == 'POST':
            if 'save-client' in request.POST:
                form = ClientForm(request.POST, instance=client_)
                form.save()
                return redirect('main:home')
    else:
        if request.method == 'GET':
            form = ClientForm()
            return render(request, '../templates/services/client.html', {'form': form})
        elif request.method == 'POST':
            if 'save-client' in request.POST:
                form = ClientForm(request.POST)
                form.save()
                return redirect('main:home')


@login_required
def new_client(request):
    if request.method == 'GET':
        return client(request, None)
    elif request.method == 'POST':
        return client(request, None)


@login_required
def detail(request, detail_pk):
    if detail_pk:
        detail_ = SparePart.objects.get(pk_spare_part=detail_pk)
        if request.method == 'GET':
            form = SparePartForm(instance=detail_)
            return render(request, '../templates/services/detail.html', {'form': form, 'change': True})
        elif request.method == 'POST':
            if 'save-detail' in request.POST:
                form = SparePartForm(request.POST, instance=detail_)
                form.save()
                return redirect('main:home')
            elif 'buy-detail' in request.POST:
                if int(request.POST['amount']) > 0:
                    detail_.amount += int(request.POST['amount'])
                    detail_.save()
                return HttpResponseRedirect(request.path_info)
    else:
        if request.method == 'GET':
            form = SparePartForm()
            return render(request, '../templates/services/detail.html', {'form': form})
        elif request.method == 'POST':
            if 'save-detail' in request.POST:
                form = SparePartForm(request.POST)
                form.save()
                return redirect('main:home')


@login_required
def new_detail(request):
    if request.method == 'GET':
        return detail(request, None)
    elif request.method == 'POST':
        return detail(request, None)


@login_required
def document(request, document_type, document_pk):
    if document_type == 'acceptance':
        form = AcceptanceDocumentForm
    elif document_type == 'fixing_document':
        form = FixingDocumentForm
    elif document_type == 'fixing_report':
        form = FixingReportForm
    elif document_type == 'return':
        form = ReturnDocumentForm
    elif document_type == 'expert':
        form = ExpertReportForm

    if document_type == 'acceptance':
        document_ = ProductAcceptanceDocument.objects.get(pk_acceptance=document_pk)
        product_ = document_.pk_product
    elif document_type == 'fixing_document':
        document_ = FixingDocument.objects.get(pk_fixing_document=document_pk)
        product_ = document_.pk_acceptance.pk_product
    elif document_type == 'fixing_report':
        document_ = FixingReport.objects.get(pk_fixing_report=document_pk)
        product_ = document_.pk_acceptance.pk_product
    elif document_type == 'return':
        document_ = ProductReturnDocument.objects.get(pk_product_return_document=document_pk)
        product_ = document_.pk_product
    elif document_type == 'expert':
        document_ = ExpertReport.objects.get(pk_expert_report=document_pk)
        product_ = document_.pk_acceptance.pk_product

    if request.method == 'GET':
        form_ = form(instance=document_)
        dictionary = {'form': form_, 'change': True, 'doc_type': document_type, 'document': document_}
        if document_type == 'fixing_report':
            parts = PartReport.objects.filter(pk_fixing_report=document_.pk_fixing_report)
            real_parts = [SparePart.objects.get(pk_spare_part=part.pk_spare_part.pk_spare_part) for part in parts]
            dictionary['parts'] = real_parts
            dictionary['choose_part'] = ChoosePartForm()
        return render(request, '../templates/services/document.html', dictionary)
    elif request.method == 'POST':
        if 'save-document' in request.POST:
            form_ = form(request.POST, instance=document_)
            form_.save()
            request.method = 'GET'
            return product(request, product_.pk_product)
        elif 'choose-part' in request.POST:
            part = ChoosePartForm(request.POST)
            spare_part = SparePart.objects.get(pk_spare_part=part.data['part'])
            spare_part.amount -= 1
            spare_part.save()
            part_report = PartReport(pk_fixing_report=document_, pk_spare_part=spare_part,
                                     pk_acceptance=document_.pk_acceptance, price=spare_part.price)
            part_report.save()
            return HttpResponseRedirect(request.path_info)


@login_required
def new_document(request, document_type, product_pk):
    if document_type == 'acceptance':
        form = AcceptanceDocumentForm
    elif document_type == 'fixing_document':
        form = FixingDocumentForm
    elif document_type == 'fixing_report':
        form = FixingReportForm
    elif document_type == 'return':
        form = ReturnDocumentForm
    elif document_type == 'expert':
        form = ExpertReportForm
    if request.method == 'GET':
        form_ = form()
        return render(request, '../templates/services/document.html', {'form': form_})
    elif request.method == 'POST':
        if 'save-document' in request.POST:
            form_ = form(request.POST)
            doc = form_.save(commit=False)
            # TODO
            # добавить переходы состояний
            # автозаполнение объектов
            if document_type == 'acceptance':
                doc.pk_product = Product.objects.get(pk_product=product_pk)
                doc.pk_consultant = Consultant.objects.get(consultant_number=UserExtent.objects.get(user=request.user).user_extent)
                doc.product_sale_date = Product.objects.get(pk_product=product_pk).warranty_start_date
                doc.save()
                pr = Product.objects.get(pk_product=product_pk)
                pr.product_status = 'OC'
                pr.save()
            elif document_type == 'fixing_document':
                doc.pk_acceptance = ProductAcceptanceDocument.objects.filter(pk_product=product_pk).order_by('-document_date')[0]
                doc.save()
                pr = Product.objects.get(pk_product=product_pk)
                pr.product_status = 'OC2'
                pr.save()
            elif document_type == 'fixing_report':
                doc.pk_acceptance = ProductAcceptanceDocument.objects.filter(pk_product=product_pk).order_by('-document_date')[0]
                doc.pk_master = Master.objects.get(master_number=UserExtent.objects.get(user=request.user).user_extent)
                doc.save()
                pr = Product.objects.get(pk_product=product_pk)
                pr.product_status = 'OM'
                pr.save()
            elif document_type == 'return':
                doc.pk_consultant = Consultant.objects.get(consultant_number=UserExtent.objects.get(user=request.user).user_extent)
                doc.pk_product = Product.objects.get(pk_product=product_pk)
                doc.save()
                pr = Product.objects.get(pk_product=product_pk)
                pr.product_status = 'U'
                pr.save()
            elif document_type == 'expert':
                doc.pk_expert = Expert.objects.get(expert_number=UserExtent.objects.get(user=request.user).user_extent)
                doc.pk_acceptance = ProductAcceptanceDocument.objects.filter(pk_product=product_pk).order_by('-document_date')[0]
                doc.save()
                pr = Product.objects.get(pk_product=product_pk)
                pr.product_status = 'OE'
                pr.save()
            request.method = 'GET'
            return product(request, product_pk)


@login_required
def print_doc(request, document_type, document_pk):
    if request.method == 'GET':
        if document_type == 'acceptance':
            doc = ProductAcceptanceDocument.objects.get(pk_acceptance=document_pk)
        elif document_type == 'fixing_document':
            doc = FixingDocument.objects.get(pk_fixing_document=document_pk)
        elif document_type == 'fixing_report':
            doc = FixingReport.objects.get(pk_fixing_report=document_pk)
        elif document_type == 'return':
            doc = ProductReturnDocument.objects.get(pk_product_return_document=document_pk)
        elif document_type == 'expert':
            doc = ExpertReport.objects.get(pk_expert_report=document_pk)

        return render(request, '../templates/services/print.html', {'document': doc})

