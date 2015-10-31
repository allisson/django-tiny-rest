# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from qurl import qurl


class PaginationMixin(object):

    paginate_by = 10

    def paginate_objects(self, request, objects):
        paginator = Paginator(objects, self.paginate_by)
        page = request.GET.get('page', 1)

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        pagination = {
            'count': object_list.paginator.count,
            'num_pages': object_list.paginator.num_pages,
            'previous_page_number': None,
            'previous_url': None,
            'next_page_number': None,
            'next_url': None
        }
        url = request.get_full_path()

        if object_list.has_next():
            next_page_number = object_list.next_page_number()
            pagination['next_page_number'] = next_page_number
            pagination['next_url'] = 'http://{0}{1}'.format(
                request.get_host(),
                qurl(
                    url,
                    add={'page': object_list.next_page_number()}
                )
            )

        if object_list.has_previous():
            previous_page_number = object_list.previous_page_number()
            pagination['previous_page_number'] = previous_page_number
            pagination['previous_url'] = 'http://{0}{1}'.format(
                request.get_host(),
                qurl(
                    url,
                    add={'page': object_list.previous_page_number()}
                )
            )

        return object_list, pagination
