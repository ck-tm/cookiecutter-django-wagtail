from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


from wagtailmetadata.models import WagtailImageMetadataMixin, MetadataMixin, MetadataPageMixin
from {{cookiecutter.project_slug}}.home import blocks

from cookie_consent.models import CookieGroup


class CustomPage(MetadataPageMixin, Page):
    header_image = models.ForeignKey('wagtailimages.Image', null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL,
                                           related_name='+')
    page_body = StreamField(
        blocks.BaseStreamBlock(), verbose_name="page_body", use_json_field=True, null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('page_body'),

    ]

    # promote_panels = SEOPage.promote_panels + [
    # ]

    # promote_panels = [
    #     MultiFieldPanel(promote_panels, "Common page configuration"),
    # ]

    class Meta:
        abstract = True


class HomePage(MetadataPageMixin, Page):
    pass


class AboutPage(CustomPage):
    subpage_types = []

    content_panels = [
        FieldPanel('title'),
        FieldPanel('header_image'),

        FieldPanel('page_body'),
    ]

    class Meta:
        verbose_name = 'Despre'
        verbose_name_plural = 'Despre'

    def get_context(self, request):
        context = super().get_context(request)
        context['logo_class'] = self.logo_class
        return context


class ContactPage(CustomPage):
    subpage_types = []
    content_panels = [
        FieldPanel('title'),
        FieldPanel('header_image'),
        FieldPanel('page_body'),
    ]

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

    def get_context(self, request):
        context = super().get_context(request)
        context['logo_class'] = self.logo_class
        return context


class TermsAndConditionsPage(CustomPage):
    subpage_types = []
    content_panels = [
        FieldPanel('title'),
        FieldPanel('page_body'),
    ]

    class Meta:
        verbose_name = _('Terms and Conditions')
        verbose_name_plural = _('Terms and Conditions')


class CookiesPage(CustomPage):
    content_panels = [
        FieldPanel('title'),
        FieldPanel('page_body'),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['cookies'] = CookieGroup.objects.all()
        return context
