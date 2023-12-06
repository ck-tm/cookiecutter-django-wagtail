from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import JsonResponse

from wagtail.models import Site

from {{cookiecutter.project_slug}}.home import models

from datetime import timedelta, datetime

import imghdr
from wsgiref.util import FileWrapper

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import View

from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError
from wagtail.images.utils import verify_signature


class RobotsView(TemplateView):

    content_type = 'text/plain'
    template_name = 'robots.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = context['view'].request
        context['wagtail_site'] = Site.find_for_request(request)
        return context


def download_ical(request, event_id):
    event = models.EventPage.objects.get(pk=event_id)
    response = HttpResponse(event.ical, content_type='text/calendar')
    response['Filename'] = 'event.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=event.ics'
    return response


class ServeImagesView(View):
    model = get_image_model()
    action = "serve"
    key = None

    @classonlymethod
    def as_view(cls, **initkwargs):
        if "action" in initkwargs:
            if initkwargs["action"] not in ["serve", "redirect"]:
                raise ImproperlyConfigured(
                    "ServeView action must be either 'serve' or 'redirect'"
                )

        return super().as_view(**initkwargs)

    @method_decorator(cache_control(max_age=3600, public=True))
    def get(self, request, signature, image_id, filter_spec, filename=None):
        if not verify_signature(
            signature.encode(), image_id, filter_spec, key=self.key
        ):
            raise PermissionDenied
        image = get_object_or_404(self.model, id=image_id)

        # Get/generate the rendition
        try:
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse(
                "Source image file not found", content_type="text/plain", status=410
            )
        except InvalidFilterSpecError:
            return HttpResponse(
                "Invalid filter spec: " + filter_spec,
                content_type="text/plain",
                status=400,
            )

        return getattr(self, self.action)(rendition)

    def serve(self, rendition):
        # Open and serve the file
        rendition.file.open("rb")
        image_format = imghdr.what(rendition.file)
        if image_format:
            return StreamingHttpResponse(
                FileWrapper(rendition.file), content_type="image/" + image_format
            )
        else:
            return StreamingHttpResponse(
                FileWrapper(rendition.file), content_type="image/jpg"
            )

    def redirect(self, rendition):
        # Redirect to the file's public location
        return redirect(rendition.url)
