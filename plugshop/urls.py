from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *
from .exceptions import NoUrlFound

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='plugshop'),
    url(r'^products/$', ProductListView.as_view(),
        name='plugshop-product-list'),

    #categories
    url(r'^categories/$', CategoryListView.as_view(),
        name='plugshop-caterory-list'),
    url(r'^products/(?P<category_path>[\-\/\w]+)/$', CategoryView.as_view(),
        name='plugshop-category'),

    #products
    url(r'^products/(?P<category_path>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$',
        ProductView.as_view(), name='plugshop-product'),

    url(r'^cart/$', CartView.as_view(), name='plugshop-cart'),
    url(r'^order/(?P<number>[\-\/\w]+)$', OrderView.as_view(),
        name='plugshop-order'),
    url(r'^order/$', OrderCreateView.as_view(), name='plugshop-order-new'),
]

def get_url(name):
    patterns = list(filter(lambda x: x.name == name, urlpatterns))

    try:
        pattern = patterns[0].pattern
    except IndexError:
        raise NoUrlFound(_("No url with name '%s'") % name)

    return pattern._regex
