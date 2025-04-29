from django import template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.paginator import Page as PaginatorPage
from wagtail.models import Page, Site

from texsite.core.models import BasePage


register = template.Library()


@register.simple_tag
def get_footer_pages(site: Site) -> list[BasePage]:
    return BasePage.objects.in_site(site).live().filter(show_in_footer=True)


@register.simple_tag
def get_menu_pages(site: Site) -> list[BasePage]:
    return BasePage.objects.in_site(site).live().filter(show_in_menus=True)


@register.simple_tag
def get_live_descendant_pages(
    parent: Page, limit: int = 0, newest_first: bool = False
) -> list[Page]:
    order_by = '-first_published_at' if newest_first else 'first_published_at'

    return parent.get_descendants().live().order_by(order_by)[:limit]


@register.simple_tag
def get_paginator(
    requested_page: str, pages: list[Page], per_page: int
) -> PaginatorPage:
    paginator = Paginator(pages, per_page)

    try:
        paginator_page = paginator.page(requested_page)
    except PageNotAnInteger:
        paginator_page = paginator.page(1)
    except EmptyPage:
        paginator_page = paginator.page(paginator.num_pages)

    return paginator_page
