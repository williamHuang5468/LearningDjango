from django.shortcuts import redirect, render
from lists.models import Item, List


def home(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list1 = List.objects.get(id=list_id)
    return render(request, 'lists.html', {'list': list1})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


def add_item(request, list_id):
    list1 = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list1)
    return redirect('/lists/%d/' % (list1.id, ))
