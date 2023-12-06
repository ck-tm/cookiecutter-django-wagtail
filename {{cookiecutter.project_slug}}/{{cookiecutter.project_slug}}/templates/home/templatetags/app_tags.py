from collections import deque
from django.contrib.contenttypes.models import ContentType
from pprint import pprint
from wagtail.images.views.serve import generate_image_url
from django import template
from django.shortcuts import reverse
from django.utils import translation, timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags, format_html
from django.db.models import Q
from {{cookiecutter.project_slug}}.home import models
from datetime import datetime, timedelta
register = template.Library()




@register.filter('generate_slug')
def generate_slug(item):
    return slugify(item, allow_unicode=False)


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.filter
def get_dict_value(d, key):
    return d.get(key, '')


@register.simple_tag(takes_context=True)
def pageurl(context, page, fallback=None):
    """
    Outputs a page's URL as relative (/foo/bar/) if it's within the same site as the
    current page, or absolute (http://example.com/foo/bar/) if not.
    If kwargs contains a fallback view name and page is None, the fallback view url will be returned.
    """
    if page is None or page == '':
        if fallback:
            return reverse(fallback)
        return ''

    if not hasattr(page, 'relative_url'):
        raise ValueError("pageurl tag expected a Page object, got %r" % page)

    try:
        current_site = context['request'].site
    except (KeyError, AttributeError):
        # request.site not available in the current context; fall back on
        # page.url
        return page.url

    # Pass page.relative_url the request object, which may contain a cached copy of
    # Site.get_site_root_paths()
    # This avoids page.relative_url having to make a database/cache fetch for this list
    # each time it's called.
    return page.relative_url(current_site, request=context.get('request'))


@register.filter('view_document')
def view_document(url):
    if url.endswith(('.pdf', '.jpg', '.png', '.jpeg')):
        return url.replace('documents/', 'document/view/'), True
    return url, False


@register.filter('get_image_url')
def get_image_url(img, spec):
    if img:
        # return 'NO'
        return generate_image_url(img, spec)




@register.simple_tag(takes_context=True)
def canonical(context):
    page = context['self']
    if not page:
        return ''
    else:
        return format_html(f'<link rel="canonical" href="{page.full_url}">')


@register.simple_tag
def get_cookies_page(language):
    try:
        page = models.CookiesPage.objects.live()[0]
        return '/' + '/'.join(page.url.split('/')[3:])
    except:
        return '#'
