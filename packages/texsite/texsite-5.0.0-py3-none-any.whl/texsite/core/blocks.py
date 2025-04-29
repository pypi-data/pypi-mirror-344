from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    IntegerBlock,
    PageChooserBlock,
    StructBlock,
    TextBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(StructBlock):
    title = CharBlock(required=True)
    subtitle = CharBlock(required=False)

    class Meta:
        icon = 'placeholder'


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)

    class Meta:
        icon = 'image'


class IntroBlock(StructBlock):
    keyvisual = ImageChooserBlock(required=False)
    slogan = CharBlock(required=True)

    class Meta:
        icon = 'placeholder'


class QuoteBlock(StructBlock):
    quote = TextBlock(required=True)
    originator = CharBlock(required=False)

    class Meta:
        icon = 'openquote'


class CodeBlock(StructBlock):
    code = TextBlock(required=True)
    language = CharBlock(required=False)

    class Meta:
        icon = 'code'


class PromotedPageBlock(StructBlock):
    page = PageChooserBlock(required=True)
    teaser = ImageChooserBlock(required=True)

    class Meta:
        icon = 'placeholder'


class ArticleListingBlock(StructBlock):
    parent = PageChooserBlock()
    limit = IntegerBlock(required=False, min_value=1)
    newest_first = BooleanBlock(default=True, required=False)

    class Meta:
        icon = 'list-ul'
