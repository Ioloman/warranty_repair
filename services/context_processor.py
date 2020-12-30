from .models import UserExtent, Consultant, Master, Expert, Product


def data(request):
    try:
        employee_number = UserExtent.objects.get(user=request.user).user_extent
        if Expert.objects.filter(expert_number=employee_number):
            employee_type = 'expert'
            status = ['WE', 'OC']
        if Consultant.objects.filter(consultant_number=employee_number):
            employee_type = 'consultant'
            status = ['WC', 'WR', 'OE', 'OM']
        if Master.objects.filter(master_number=employee_number):
            employee_type = 'master'
            status = ['WF', 'OC2']

        products_urgent = []
        for st in status:
            products_urgent.extend(list(Product.objects.filter(product_status=st)))

        products = set(Product.objects.all())
        products -= set(products_urgent)
        products = list(products)
        return {'products': products, 'employee': employee_type, 'urgent': products_urgent}

    except TypeError:
        return {}