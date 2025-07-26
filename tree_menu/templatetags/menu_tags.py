from django import template
from django.utils.safestring import mark_safe
from ..models import Menu, MenuItem

register = template.Library()


def build_menu_tree(menu_items, current_url):
    tree = {}
    root_items = []
    active_path = set()
    
    for item in menu_items:
        if item.parent_id is None:
            root_items.append(item)
        else:
            if item.parent_id not in tree:
                tree[item.parent_id] = []
            tree[item.parent_id].append(item)
    
    def find_active_path(items):
        for item in items:
            item_url = item.get_absolute_url()
            if current_url and (item_url == current_url or 
                               (item.url and current_url.startswith(item.url) and item.url != '/')):
                active_path.add(item.id)
                parent = item.parent
                while parent:
                    active_path.add(parent.id)
                    parent = parent.parent
                return True
            
            children = tree.get(item.id, [])
            if find_active_path(children):
                active_path.add(item.id)
                return True
        return False
    
    find_active_path(root_items)
    
    def build_tree_nodes(items, level=0):
        result = []
        for item in items:
            children = tree.get(item.id, [])
            is_in_path = item.id in active_path
            
            should_expand = (is_in_path or 
                           any(child.id in active_path for child in children))
            
            node = {
                'item': item,
                'children': build_tree_nodes(children, level + 1) if should_expand else [],
                'is_active': current_url and item.get_absolute_url() == current_url,
                'is_in_path': is_in_path,
                'level': level,
                'has_children': bool(children),
                'is_expanded': should_expand
            }
            result.append(node)
        
        return result
    
    return build_tree_nodes(root_items)


def render_menu_html(tree_nodes, css_class='menu'):
    if not tree_nodes:
        return ''
    
    html = f'<ul class="{css_class}">'
    
    for node in tree_nodes:
        item = node['item']
        css_classes = []
        
        if node['is_active']:
            css_classes.append('active')
        if node['is_in_path']:
            css_classes.append('in-path')
        if node['has_children']:
            css_classes.append('has-children')
        if node['is_expanded']:
            css_classes.append('expanded')
        
        class_attr = f' class="{" ".join(css_classes)}"' if css_classes else ''
        
        html += f'<li{class_attr}>'
        html += f'<a href="{item.get_absolute_url()}">{item.title}</a>'
        
        if node['children']:
            html += render_menu_html(node['children'], 'submenu')
        
        html += '</li>'
    
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    current_url = request.path if request else ''
    
    try:
        menu = Menu.objects.get(name=menu_name)
        menu_items = list(MenuItem.objects.filter(menu=menu).select_related('parent'))
        tree = build_menu_tree(menu_items, current_url)
        return mark_safe(render_menu_html(tree))
    except Menu.DoesNotExist:
        return ''
