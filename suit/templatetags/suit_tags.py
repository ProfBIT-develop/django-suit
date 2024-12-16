import itertools
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from suit.config import get_config
from suit import utils

try:
    from django.core.urlresolvers import NoReverseMatch, reverse
except (ImportError, ModuleNotFoundError):
    from django.urls import NoReverseMatch, reverse

django_version = utils.django_major_version()

try:
    # Django 1.9
    from django.contrib.admin.utils import lookup_field
except ImportError:
    from django.contrib.admin.util import lookup_field

register = template.Library()

if django_version < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@register.filter(name='suit_conf')
def suit_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.tag
def suit_date(parser, token):
    return NowNode(get_config('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(get_config('HEADER_TIME_FORMAT'))


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.object_name.lower())
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def suit_bc(*args):
    return utils.value_by_version(args)


@simple_tag
def suit_bc_value(*args):
    return utils.value_by_version(args)


@simple_tag
def admin_extra_filters(cl):
    """ Return the dict of used filters which is not included
    in list_filters form """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys()
                                             for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@simple_tag
def suit_django_version():
    return django_version


@register.filter
def django_version_lt(string):
    return django_version < str_to_version(string)


@register.filter
def django_version_lte(string):
    return django_version <= str_to_version(string)


@register.filter
def django_version_gt(string):
    return django_version > str_to_version(string)


@register.filter
def django_version_gte(string):
    return django_version >= str_to_version(string)


def str_to_version(string):
    return tuple([int(s) for s in string.split('.')])


if django_version < (1, 9):
    # Add empty tags to avoid Django template errors if < Django 1.9
    @register.simple_tag
    def add_preserved_filters(*args, **kwargs):
        pass

if django_version < (1, 5):
    # Add admin_urlquote filter to support Django 1.4
    from django.contrib.admin.util import quote


    @register.filter
    def admin_urlquote(value):
        return quote(value)

if django_version >= (5, 1):
    @register.filter
    def length_is(value, arg):
        """Return a boolean of whether the value's length is the argument."""
        try:
            return len(value) == int(arg)
        except (ValueError, TypeError):
            return ''