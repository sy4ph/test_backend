from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ('title', 'parent', 'url', 'named_url', 'order')
    

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'get_absolute_url', 'order')
    list_filter = ('menu', 'parent')
    list_editable = ('order',)
    search_fields = ('title', 'url', 'named_url')
    fields = ('menu', 'title', 'parent', 'url', 'named_url', 'order')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('menu', 'parent')
    
    def save_model(self, request, obj, form, change):
        if obj.url and not obj.url.startswith('/'):
            obj.url = '/' + obj.url
        if obj.url and not obj.url.endswith('/'):
            obj.url = obj.url + '/'
        super().save_model(request, obj, form, change)
