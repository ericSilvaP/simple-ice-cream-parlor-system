from django.db.models import Q


def filter_orders(
    request, orders, search_term, min_value=0, max_value=0, status_list=[]
):
    if search_term:
        if str(search_term).isdigit():
            orders = orders.filter(pk__icontains=search_term)
        else:
            orders = orders.filter(
                Q(user__username__icontains=search_term)
                | Q(items__product__name__icontains=search_term)
            )

    if not min_value and max_value:
        orders = orders.filter(total_value__lte=max_value)
    elif not max_value and min_value:
        orders = orders.filter(total_value__gte=min_value)
    if min_value and max_value:
        if int(min_value) < int(max_value):
            orders = orders.filter(
                total_value__gte=min_value, total_value__lte=max_value
            )

    status_search_list = []
    for status in status_list:
        if status == "Completo" and request.GET.get(status):
            status_search_list.append("complete")
        if status == "Cancelado" and request.GET.get(status):
            status_search_list.append("canceled")
        if status == "Pendente" and request.GET.get(status):
            status_search_list.append("pending")

    if status_search_list:
        orders = orders.filter(status__in=status_search_list)

    return orders, search_term


def filter_products(
    products, search_term, min_value=0, max_value=0, categories_filter_list=[]
):
    if search_term:
        products = products.filter(name__icontains=search_term)

    if not min_value and max_value:
        products = products.filter(price__lte=max_value)
    elif not max_value and min_value:
        products = products.filter(price__gte=min_value)
    if min_value and max_value:
        if int(min_value) < int(max_value):
            products = products.filter(price__gte=min_value, price__lte=max_value)

    if categories_filter_list:
        products = products.filter(category__name__in=categories_filter_list)

    return products, search_term
