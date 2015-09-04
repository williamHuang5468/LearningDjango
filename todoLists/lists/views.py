from django.shortcuts import redirect, render
from lists.models import Item, List


def home(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list1 = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list1)
    return render(request, 'lists.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
