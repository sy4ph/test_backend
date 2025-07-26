from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from .models import MenuItem


def home(request):
    return render(request, 'base.html', {
        'page_title': 'Home Page',
        'page_content': 'This is Home page.'
    })


def admin_redirect(request):
    return redirect('/admin/')


def dynamic_page(request, page_path):
    if not page_path.startswith('/'):
        page_path = '/' + page_path
    
    if not page_path.endswith('/'):
        page_path = page_path + '/'
    
    if page_path == '/home/':
        return render(request, 'base.html', {
            'page_title': 'Home Page',
            'page_content': 'This is Home page.'
        })
    
    menu_item = get_object_or_404(MenuItem, url=page_path)
    
    return render(request, 'base.html', {
        'page_title': f'{menu_item.title} Page',
        'page_content': f'This is {menu_item.title} page.',
        'menu_item': menu_item
    })
