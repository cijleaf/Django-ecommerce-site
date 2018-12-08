from django import template

register = template.Library()


class HasProduct(template.Node):
    def __init__(self, parser, token):
        tag_name, product = token.split_contents()


        nodelist = parser.parse(('endplusghop_has_product',))
        parser.delete_first_token()

        self.product = parser.compile_filter(product)
        self.nodelist = nodelist

    def render(self, context, *args, **kwargs):
        return self.nodelist.render(context)


@register.tag
def plusghop_has_product(parser, token, *args, **kwargs):
    return HasProduct(parser, token)


def plugshop_currency(value):
    if value is None:
        return ""

    v = str(value)[::-1]
    return " ".join([v[i:i+3][::-1] for i in range(0, len(v), 3)][::-1])
register.filter('plugshop_currency', plugshop_currency)


@register.inclusion_tag('plugshop/tags/action.html')
def plugshop_action(product, action, quantity=1):
    return {
        'product': product,
        'action': action,
        'quantity': quantity,
    }
