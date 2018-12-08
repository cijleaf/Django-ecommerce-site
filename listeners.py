def add_item(sender, item, price, quantity, **kwargs):
    #print 'append', item, price, quantity
    pass


def remove_item(sender, item, quantity, **kwargs):
    #print 'remove', item, quantity
    pass


def order_create_signal(sender, order, request, **kwargs):
    order.ip_address = request.META.get('REMOTE_ADDR', None)
    order.save()
