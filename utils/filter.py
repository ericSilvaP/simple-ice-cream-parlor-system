def filter_orders(
    request, orders, search_term, min_value=0, max_value=0, status_list=[]
):
    if search_term:
        if str(search_term).isdigit():
            orders = orders.filter(pk__icontains=search_term)
        else:
            orders = orders.filter(user__username__icontains=search_term)

    if not min_value and max_value:
        orders = orders.filter(total_value__lte=max_value)
    elif not max_value and min_value:
        orders = orders.filter(total_value__gte=min_value)
    if min_value and max_value:
        if int(min_value) < int(max_value):
            orders = orders.filter(
                total_value__gte=min_value, total_value__lte=max_value
            )

    for status in status_list:
        status_search = ""
        if status == "Completo" and request.GET.get(status):
            status_search = "complete"
        if status == "Cancelado" and request.GET.get(status):
            status_search = "canceled"
        if status == "Pendente" and request.GET.get(status):
            status_search = "pending"

        if status_search:
            orders = orders.filter(status=status_search)

    return orders, search_term
