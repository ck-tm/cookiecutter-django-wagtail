from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructValue
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.blocks import (
    CharBlock, URLBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, ListBlock, PageChooserBlock, FloatBlock
)

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField


class SocialLink(StructBlock):
    website = ChoiceBlock(choices=[
        ('', 'Select website'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
    ], blank=True, required=False, label="Website")
    link = URLBlock(required=False)


class SubMenuBlock(StructBlock):
    page = PageChooserBlock(required=False, label="Pagină")
    name = CharBlock(required=False, label="Nume")
    link = URLBlock(required=False)

    class Meta:
        icon = 'fa-caret-down'


class MenuBlock(StructBlock):
    page = PageChooserBlock(required=False, label="Pagină")
    name = CharBlock(required=False, label="Nume")
    link = URLBlock(required=False)
    submenu = ListBlock(SubMenuBlock(), required=False, label="Submeniu")

    class Meta:
        icon = 'fa-bars'


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    title = CharBlock(required=False, label="Titlu")
    image = ImageChooserBlock(required=True, label="Imagine")
    caption = CharBlock(required=False, label="Caption")

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class DocumentBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing documents with associated caption and
    attribution data
    """
    document = DocumentChooserBlock(required=True)
    title = CharBlock(required=True, label="Titlu")
    description = TextBlock(required=False, label="Descriere")

    class Meta:
        icon = 'file-text'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context


class SponsorBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=False, label="Imagine")
    name = CharBlock(required=True, label="Nume")
    link = CharBlock(max_length=500, required=True)

    class Meta:
        icon = 'user'
        # template = "blocks/sponsor_block.html"


class SectionHeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to set a heading
    """
    heading_text = CharBlock(classname="title", required=True, label="Titlu")

    class Meta:
        icon = "title"
        template = "blocks/section_heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


class EmbedBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to add an embed code (youtube, soundcloud, etc)
    """
    embed_code = TextBlock()
    iframe_aspect_ratio = ChoiceBlock(choices=[
        ('16by9', 'Select an aspect ratio'),
        ('16by9', 'Video (16/9)'),
        ('2by1', 'SoundCloud (2/1)'),
        # ('4by5', '4/5'),
        ('3by1', 'SoundCloud (3/1')
    ], blank=True, required=False)

    class Meta:
        icon = "fa-video-camera"
        template = "blocks/embed_block.html"


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = SectionHeadingBlock(label=_("Title"))
    paragraph_block = RichTextBlock(
        label="Paragraph",
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        features=['bold', 'italic', 'link', 'ol', 'ul', 'document-link'])
    image_block = ImageBlock(label="Imagine")

    carousel = ListBlock(
        ImageBlock(label=_("Image gallery")),
        label="Galerie Foto",
        icon="copy",
        template="blocks/carousel.html")

    quote_block = BlockQuote(icon="openquote")
    embed_block = EmbedBlock(icon="code")
