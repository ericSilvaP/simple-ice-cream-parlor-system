def create_products_pagination_url(
    search_term, min_value=0, max_value=0, categories=[]
):
    pagination_url = ""
    if search_term:
        pagination_url += f"&q={search_term}"
    if min_value:
        pagination_url += f"&min_value={min_value}"
    if max_value:
        pagination_url += f"&max_value={max_value}"
    for category in categories:
        pagination_url += f"&category_{category}=on"

    return pagination_url


def create_orders_pagination_url(search_term, min_value=0, max_value=0, status_list=[]):
    pagination_url = ""
    if search_term:
        pagination_url += f"&q={search_term}"
    if min_value:
        pagination_url += f"&min_value={min_value}"
    if max_value:
        pagination_url += f"&max_value={max_value}"
    for status in status_list:
        pagination_url += f"&{status}=on"

    return pagination_url
