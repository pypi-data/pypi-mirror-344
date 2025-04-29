from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField

from texsite.core.blocks import (
    ArticleListingBlock,
    CodeBlock,
    HeadingBlock,
    ImageBlock,
    IntroBlock,
    QuoteBlock,
)
from texsite.core.models import BasePage


class CleanBlogPage(BasePage):
    body = StreamField(
        [
            (
                'intro',
                IntroBlock(template='texsitecleanblog/blocks/intro.html'),
            ),
            (
                'heading',
                HeadingBlock(template='texsitecleanblog/blocks/heading.html'),
            ),
            ('paragraph', RichTextBlock()),
            (
                'image',
                ImageBlock(template='texsitecleanblog/blocks/image.html'),
            ),
            (
                'quote',
                QuoteBlock(template='texsitecleanblog/blocks/quote.html'),
            ),
            (
                'code',
                CodeBlock(template='texsitecleanblog/blocks/code.html'),
            ),
            (
                'article_listing',
                ArticleListingBlock(
                    template='texsitecleanblog/blocks/article_listing.html'
                ),
            ),
        ],
    )

    content_panels = BasePage.content_panels + [FieldPanel('body')]

    class Meta:
        verbose_name = _('Clean Blog Page') + ' (' + __package__ + ')'
