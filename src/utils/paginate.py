from math import ceil


class Paginator:
    @staticmethod
    def apply(params, total_rows):
        page = params.get("page")
        if page is None or (not page.isdigit()):
            page = 1
        page = int(page)
        if page <= 0:
            page = 1

        per_page = params.get("per_page")
        if per_page is None or (not per_page.isdigit()):
            per_page = 10
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10

        offset = (page - 1) * per_page

        return {"limit": per_page, "offset": offset, "page": page, "pages": ceil(total_rows / per_page)}
