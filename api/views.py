from django.utils.translation import get_language
from rest_framework.decorators import detail_route, api_view, renderer_classes
from rest_framework.renderers import StaticHTMLRenderer, JSONRenderer
from rest_framework import permissions, status, authentication, throttling
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.schemas import SchemaGenerator, as_query_fields
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_extensions.cache.decorators import cache_response
# from rest_framework.compat import coreapi, urlparse
# import time, json
# from django.core.signals import request_started, request_finished
# from django.http import HttpResponse
import hashlib, json

from .handler import WPHandler, WPHandlerException

# TODO add descriptions
query_params = [
    {'description': 'Add some description', 'in': 'query', 'name': 'revid', 'required': True, 'type': 'boolean'},  # 'default': 'false',
    {'description': 'Add some description', 'in': 'query', 'name': 'author', 'required': True, 'type': 'boolean'},
    {'description': 'Add some description', 'in': 'query', 'name': 'tokenid', 'required': True, 'type': 'boolean'}
]

custom_data = {
    # 'info': {'title': 'WikiWho API', 'version': ''},
    'paths':
        {'/authorship/{article_name}/':
             {'get': {'description': '# Some description \n **with** *markdown* \n\n '
                                     '[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)',
                      'parameters': [{'description': 'Add some description',
                                      'in': 'path',
                                      'name': 'article_name',
                                      'required': True,
                                      'type': 'string'},
                                     ] + query_params,
                      'responses': {'200': {'description': ''}},
                      'tags': ['authorship'],
                      'summary': 'Get authorship of last revision of article'
                      }
              },
         '/authorship/{article_name}/{revision_id}/':
             {'get': {'description': '',
                      'parameters': [{'description': '',
                                      'in': 'path',
                                      'name': 'revision_id',
                                      'required': True,
                                      'type': 'integer'},
                                     {'description': '',
                                      'in': 'path',
                                      'name': 'article_name',
                                      'required': True,
                                      'type': 'string'},
                                     ] + query_params,
                      'responses': {'200': {'description': ''}},
                      'tags': ['authorship'],
                      'summary': 'Get authorship of given revision of article'
                      }
              },
         '/authorship/{article_name}/{start_revision_id}/{end_revision_id}/':
             {'get': {'description': '',
                      'parameters': [{'description': '',
                                      'in': 'path',
                                      'name': 'end_revision_id',
                                      'required': True,
                                      'type': 'integer'},
                                     {'description': '',
                                      'in': 'path',
                                      'name': 'start_revision_id',
                                      'required': True,
                                      'type': 'integer'},
                                     {'description': '',
                                      'in': 'path',
                                      'name': 'article_name',
                                      'required': True,
                                      'type': 'string'},
                                     ] + query_params,
                      'responses': {'200': {'description': ''}},
                      'tags': ['authorship'],
                      'summary': 'Get authorship of given revisions of article'
                      }
              },
         },
}


class MyOpenAPIRenderer(OpenAPIRenderer):
    """
    Custom OpenAPIRenderer to update field types and descriptions.
    """
    def add_customizations(self, data, renderer_context):
        """
        Adds settings, overrides, etc. to the specification.
        """
        super(MyOpenAPIRenderer, self).add_customizations(data, renderer_context)
        # print(type(data), data)
        # TODO update
        data['paths'].update(custom_data['paths'])
        version = '1.0.0-beta'
        data['info']['version'] = version
        data['info']['description'] = 'A short description of the application. ' \
                                      'GFM syntax can be used for rich text representation. \n\n' \
                                      'Specification: http://swagger.io/specification \n\n' \
                                      'Example api: http://petstore.swagger.io/'
        data['info']['contact'] = {'name': 'GESIS - Leibniz Institute for the Social Sciences',
                                   # 'email': 'kenan.erdogan@gesis.org',
                                   'url': 'http://www.gesis.org/en/institute/gesis-scientific-departments/computational-social-science/'}
        data['basePath'] = '/api/v{}'.format(version)
        # print(type(data), data)


@api_view()
@renderer_classes([MyOpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request, version):
    generator = SchemaGenerator(title='WikiWho API', urlconf='api.urls')
    schema = generator.get_schema(request=request)
    # print(type(schema), schema)
    return Response(schema)


class BurstRateThrottle(throttling.UserRateThrottle):
    """
    Limit authenticated users when they burst the api. Check DEFAULT_THROTTLE_RATES settings: 100/min
    """
    scope = 'burst'


class WikiwhoApiView(ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    throttle_classes = (throttling.UserRateThrottle, throttling.AnonRateThrottle, BurstRateThrottle)
    # serializer_class = WikiWhoSerializer
    # filter_fields = ('query_option_1', 'query_option_2',)
    query_fields = ('revid', 'author', 'tokenid', )
    renderer_classes = [JSONRenderer]  # to disable browsable api

    def get_parameters(self):
        parameters = []
        if self.request.GET.get('revid') == 'true':
            parameters.append('revid')
        if self.request.GET.get('author') == 'true':
            parameters.append('author')
        if self.request.GET.get('tokenid') == 'true':
            parameters.append('tokenid')
        return parameters

    def get_response(self, article_name, parameters, revision_ids=list()):
        if not parameters:
            return Response({'Error': 'At least one query parameter should be selected.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # global handler_time
        # handler_start = time.time()
        with WPHandler(article_name) as wp:
            try:
                wp.handle(revision_ids, 'json')
            except WPHandlerException as e:
                response = {'Error': e.message}
                status_ = status.HTTP_400_BAD_REQUEST
            else:
                response = wp.wikiwho.get_revision_json(wp.revision_ids, parameters)
                status_ = status.HTTP_200_OK
        # handler_time = time.time() - handler_start
        # return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')
        return Response(response, status=status_)

    # TODO http://www.django-rest-framework.org/api-guide/renderers/
    @detail_route(renderer_classes=(StaticHTMLRenderer,))
    def get_slice(self, request, version, article_name, start_revision_id, end_revision_id):
        start_revision_id = int(start_revision_id)
        end_revision_id = int(end_revision_id)
        if start_revision_id >= end_revision_id:
            return Response({'Error': 'Second revision id has to be larger than first revision id!'},
                            status=status.HTTP_400_BAD_REQUEST)
        parameters = self.get_parameters()
        return self.get_response(article_name, parameters, [start_revision_id, end_revision_id])

    @detail_route(renderer_classes=(StaticHTMLRenderer,))
    def get_article_revision(self, request, version, article_name, revision_id):
        # TODO cache this if only rev id is the last rev id
        parameters = self.get_parameters()
        return self.get_response(article_name, parameters, [int(revision_id)])

    @cache_response(key_func='calculate_cache_key')
    @detail_route(renderer_classes=(StaticHTMLRenderer,))
    def get_article_by_name(self, request, version, article_name):
        # TODO when models are created, delete cache.delete(this_key) if last_rev_id is changed or obj is deleted!
        parameters = self.get_parameters()
        return self.get_response(article_name, parameters)

    def calculate_cache_key(self, view_instance, view_method, request, args, kwargs):
        # FIXME for different query parameters
        l = list(kwargs.values())
        l.remove(request.version)
        l.append(request.accepted_renderer.format)
        l.append(get_language())
        key = hashlib.sha256(json.dumps(l, sort_keys=True).encode('utf-8')).hexdigest()
        return key

    # @detail_route(renderer_classes=(StaticHTMLRenderer,))
    # def get_article_by_revision(self, request, revision_id):
    #     return Response({'test': 'get_article_by_revision'})

    # def dispatch(self, request, *args, **kwargs):
    #     global dispatch_time
    #     global render_time
    #
    #     dispatch_start = time.time()
    #     ret = super(WikiwhoApiView, self).dispatch(request, *args, **kwargs)
    #
    #     render_start = time.time()
    #     # ret.render()
    #     render_time = time.time() - render_start
    #
    #     dispatch_time = time.time() - dispatch_start
    #     return ret
    #
    # def started(sender, **kwargs):
    #     global started
    #     started = time.time()
    #
    # def finished(sender, **kwargs):
    #     total = time.time() - started
    #     api_view_time = dispatch_time - (render_time + handler_time)
    #     request_response_time = total - dispatch_time
    #
    #     # print ("Database lookup               | %.4fs" % db_time)
    #     # print ("Serialization                 | %.4fs" % serializer_time)
    #     print ("Django request/response       | %.4fs" % request_response_time)
    #     print ("API view                      | %.4fs" % api_view_time)
    #     print ("Response rendering            | %.4fs" % render_time)
    #     print ("handler_time                  | %.4fs" % handler_time)
    #     print ("total                         | %.4fs" % total)
    #
    # request_started.connect(started)
    # request_finished.connect(finished)


# class MySchemaGenerator(SchemaGenerator):
#     """
#     Custom SchemaGenerator to enable adding query fields.
#     """
#     def get_query_fields(self, view):
#         """
#         Return query fields of given views.
#         """
#         query_fields = getattr(view, 'query_fields', [])
#         fields = as_query_fields(query_fields)
#         return fields
#
#     def get_link(self, path, method, callback):
#         """
#         Return a `coreapi.Link` instance for the given endpoint.
#         """
#         view = callback.cls()
#
#         fields = self.get_path_fields(path, method, callback, view)
#         fields += self.get_serializer_fields(path, method, callback, view)
#         fields += self.get_pagination_fields(path, method, callback, view)
#         fields += self.get_filter_fields(path, method, callback, view)
#         # add query fields
#         fields += self.get_query_fields(view)
#
#         if fields and any([field.location in ('form', 'body') for field in fields]):
#             encoding = self.get_encoding(path, method, callback, view)
#         else:
#             encoding = None
#
#         return coreapi.Link(
#             url=urlparse.urljoin(self.url, path),
#             action=method.lower(),
#             encoding=encoding,
#             fields=fields
#         )