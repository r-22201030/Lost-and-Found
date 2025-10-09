from .models import LostItem, FoundItem

def items_for_navbar(request):
    """
    Context processor for Navbar: recent lost and found items.
    Returns dictionary with keys 'lost_items' and 'found_items'.
    """
    return {
        'lost_items': LostItem.objects.all()[:5],
        'found_items': FoundItem.objects.all()[:5],
    }
