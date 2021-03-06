# import traceback

from django.utils.timezone import now
from django.utils.translation import get_language

from .models import APIRequestLog


class LoggingMixin(object):
    logging_methods = '__all__'

    """Mixin to log requests"""
    def initial(self, request, *args, **kwargs):
        """Set current time on request"""

        # check if request method is being logged
        # if self.logging_methods != '__all__' and request.method not in self.logging_methods:
        #     super(LoggingMixin, self).initial(request, *args, **kwargs)
        #     return None

        # # get IP
        ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddr:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ipaddr = [x.strip() for x in ipaddr.split(",")][0]
        else:
            ipaddr = request.META.get("REMOTE_ADDR", "")

        # get view
        # view_name = ''
        # try:
        #     method = request.method.lower()
        #     attributes = getattr(self, method)
        #     view_name = (type(attributes.__self__).__module__ + '.' +
        #                  type(attributes.__self__).__name__)
        # except Exception:
        #     pass

        # get the method of the view
        if hasattr(self, 'action'):
            view_method = self.action if self.action else ''
        else:
            # get url name as view method
            view_method = request.resolver_match.url_name

        # save to log
        self.request.log = APIRequestLog(
            requested_at=now(),
            # path=request.path,
            # view=view_name,
            view_method=view_method,
            view_class=self.__class__.__name__,
            remote_addr=ipaddr,
            # host=request.get_host(),
            # method=request.method,
            query_params=request.query_params.dict().__str__()[:256],
            language=get_language()
        )

        # regular initial, including auth check
        super(LoggingMixin, self).initial(request, *args, **kwargs)

        # add user to log after auth
        # user = request.user
        # if user.is_anonymous():
        #     user = None
        # self.request.log.user = user

        # get data dict
        # try:
        #     # Accessing request.data *for the first time* parses the request body, which may raise
        #     # ParseError and UnsupportedMediaType exceptions. It's important not to swallow these,
        #     # as (depending on implementation details) they may only get raised this once, and
        #     # DRF logic needs them to be raised by the view for error handling to work correctly.
        #     self.request.log.data = self.request.data.dict()
        # except AttributeError:  # if already a dict, can't dictify
        #     self.request.log.data = self.request.data
        # finally:
        #     self.request.log.save()

    # def handle_exception(self, exc):
    #     # basic handling
    #     response = super(LoggingMixin, self).handle_exception(exc)
    #
    #     # log error
    #     self.request.log.errors = traceback.format_exc()
    #     self.request.log.status_code = response.status_code
    #     self.request.log.save()
    #
    #     # return
    #     return response

    def finalize_response(self, request, response, *args, **kwargs):
        # regular finalize response
        response = super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)

        # check if request method is being logged
        # if self.logging_methods != '__all__' and request.method not in self.logging_methods:
        #     return response

        # add user to log after auth
        # user = request.user
        # if user.is_anonymous():
        #     user = None
        # self.request.log.user = user

        # compute response time
        response_timedelta = now() - self.request.log.requested_at
        response_ms = int(response_timedelta.total_seconds() * 1000)

        # save to log
        # self.request.log.response = response.rendered_content
        self.request.log.status_code = response.status_code
        self.request.log.response_ms = response_ms
        
        # priorizes page_id as the main instance in the log
        if hasattr(self, 'page_id'):
            self.request.log.instance_id = self.page_id
            self.request.log.type_id = 'page_id'
        elif hasattr(self, 'editor_id'):
            self.request.log.instance_id = self.editor_id
            self.request.log.type_id = 'editor_id'
        elif hasattr(self, 'rev_id'):
            self.request.log.instance_id = self.rev_id
            self.request.log.type_id = 'rev_id'
        
        # self.request.log.save(update_fields=['user', 'status_code', 'response_ms', 'page_id'])
        self.request.log.save()

        # return
        return response
