from django.shortcuts import redirect, render
from lists.models import Item


def home(request):
    return render(request, 'home.html')

'''
def home(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    return render(request, 'home.html')
'''
def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists.html', {'items': items})

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')

