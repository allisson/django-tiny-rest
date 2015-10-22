# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser

from qurl import qurl
import status

from tiny_rest.http import JsonResponse
from tiny_rest.constants import SAFE_METHODS


class APIView(View):

    paginate_by = 20
    lookup_field = 'pk'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.pk = self.kwargs.get(self.lookup_field, None)

        self.patch_request_method(request)
        self.authenticate(request)
        if not self.authorize(request):
            return self.not_authorized()

        return super(APIView, self).dispatch(request, *args, **kwargs)

    def patch_request_method(self, request):
        # if request.method != 'POST' and request.method != 'GET':
        if request.method not in SAFE_METHODS + ('POST', ):
            method = request.method
            request.method = 'POST'
            request._load_post_and_files()
            request.method = method
            setattr(request, method, request.POST)

    def authenticate(self, request):
        if request.user.is_authenticated() and not request.user.is_active:
            request.user = AnonymousUser()

    def authorize(self, request):
        return True

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

    def get(self, request, *args, **kwargs):
        if self.pk:
            return self.detail(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.pk:
            return self.method_not_allowed()
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.pk:
            return self.update(request, *args, **kwargs)
        return self.method_not_allowed()

    def patch(self, request, *args, **kwargs):
        if self.pk:
            return self.partial_update(request, *args, **kwargs)
        return self.method_not_allowed()

    def delete(self, request, *args, **kwargs):
        if self.pk:
            return self.destroy(request, *args, **kwargs)
        return self.method_not_allowed()

    def list(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def create(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def detail(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def update(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def partial_update(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def destroy(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def response(self, data={}, status_code=200):
        return JsonResponse(data=data, status=status_code)

    def not_authorized(self):
        data = {'error': _('Not Authorized')}
        return self.response(data=data, status_code=status.HTTP_403_FORBIDDEN)

    def method_not_allowed(self):
        data = {'error': _('Method Not Allowed')}
        return self.response(
            data=data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def resource_not_found(self):
        data = {'error': _('Resource Not Found')}
        return self.response(data=data, status_code=status.HTTP_404_NOT_FOUND)
