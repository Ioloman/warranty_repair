from django.urls import path
from services import views as s_views


app_name = 'main'

urlpatterns = [
    path('home/', s_views.home, name='home'),
    path('list/', s_views.product_list, name='product_list'),
    path('product/<int:product_pk>', s_views.product, name='product'),
    path('client/<int:client_pk>', s_views.client, name='client'),
    path('client/new', s_views.new_client, name='new_client'),
    path('detail/<int:detail_pk>', s_views.detail, name='detail'),
    path('detail/new', s_views.new_detail, name='new_detail'),
    path('document/<str:document_type>/<int:document_pk>', s_views.document, name='document'),
    path('document/<str:document_type>/new?pr_id=<int:product_pk>', s_views.new_document, name='new_document'),
    path('printdocument/<str:document_type>/<int:document_pk>', s_views.print_doc, name='print'),
]