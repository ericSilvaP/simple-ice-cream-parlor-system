from math import ceil


def make_pagination_range(
    page_range,
    pages_qnt,
    current_page,
):
    middle = ceil(pages_qnt / 2)
    total_pages = len(page_range)

    # início fixo
    if current_page <= middle:
        pagination = page_range[:pages_qnt]

    # final fixo
    elif current_page + middle > total_pages:
        pagination = page_range[-pages_qnt:]

    else:
        # meio dinâmico (centraliza current_page)
        start = current_page - middle
        end = start + pages_qnt

        pagination = page_range[start:end]

    return {
        "pagination": pagination,
        "page_range": page_range,
        "qty_pages": pages_qnt,
        "current_page": current_page,
        "total_pages": total_pages,
        "first_page_out_of_range": current_page > middle,
        "last_page_out_of_range": current_page + middle < total_pages,
    }
