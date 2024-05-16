from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    return render(request, 'links/home.html')

def table(request):
    search = request.GET.get('search')
    sort_by = request.GET.get('sort')

    data = Inventory.objects.all()

    if search:
        data = data.filter(
            Q(brand__icontains=search) |
            Q(type__icontains=search) |
            Q(productName__icontains=search) |
            Q(desc__icontains=search) |
            Q(price__icontains=search) |
            Q(quantity__icontains=search)
        )

    if sort_by:
        field, order = sort_by.split('_')
        if order == 'asc':
            data = data.order_by(field)
        else:
            data = data.order_by(f'-{field}')
            
    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data': data,
        'search': search
    }
    return render(request, 'links/table.html', context)

def create(request):
    data = Inventory.objects.all()
    context = {
        'data': data,
        'content': request.POST,
    }
    if request.method == 'GET':
        return render(request, 'links/create.html', context)

    if request.method == 'POST':
        brand = request.POST.get('brand')
        type = request.POST.get('type')
        productName = request.POST.get('productName')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([brand, type, productName, desc, price, quantity]):
            messages.error(request, 'Must fill up all fields')
            return render(request, 'links/create.html', context)
        
        if Inventory.objects.filter(productName__iexact=productName).exists():
            messages.error(request, 'Product name must be unique (case-insensitive)')
            return render(request, 'links/create.html', context)
        
        Inventory.objects.create(
            brand=brand, type=type, productName=productName,
            desc=desc, price=price, quantity=quantity
        )
        messages.success(request, productName + ' created successfully')
        return redirect('create')

def edit(request, id):
    data = get_object_or_404(Inventory, pk=id)
    context = {
        'data': data,
    }
    
    if request.method == 'GET':
        return render(request, 'links/edit.html', context)

    if request.method == 'POST':
        brand = request.POST.get('brand')
        type = request.POST.get('type')
        productName = request.POST.get('productName')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        if not all([brand, type, productName, desc, price, quantity]):
            messages.error(request, 'Must fill up all fields')
            return render(request, 'links/edit.html', context)
        
        if Inventory.objects.filter(productName__iexact=productName).exclude(pk=id).exists():
            messages.error(request, 'Product name must be unique (case-insensitive)')
            return render(request, 'links/edit.html', context)

        data.brand = brand
        data.type = type
        data.productName = productName
        data.desc = desc
        data.price = price
        data.quantity = quantity
        data.save()

        messages.success(request, 'Data updated successfully')
        return redirect('edit', id=id)

def delete(request, id):
    data = Inventory.objects.get(pk=id)
    data.delete()
    messages.success(request, 'Data removed')
    return redirect('table')

def graph(request):
    graph_type = request.GET.get('graph_type', 'Product')
    labels = []
    data = []

    if graph_type == 'Product':
        queryset = Inventory.objects.values('productName').annotate(total=Sum('quantity'))
        for item in queryset:
            labels.append(item['productName'])
            data.append(item['total'])
    elif graph_type == 'Brand':
        queryset = Inventory.objects.values('brand').annotate(total=Sum('quantity'))
        for item in queryset:
            labels.append(item['brand'])
            data.append(item['total'])
    elif graph_type == 'Type':
        queryset = Inventory.objects.values('type').annotate(total=Sum('quantity'))
        for item in queryset:
            labels.append(item['type'])
            data.append(item['total'])

    context = {
        'labels': labels,
        'data': data,
        'graph_type': graph_type,
    }
    return render(request, 'links/graph.html', context)
