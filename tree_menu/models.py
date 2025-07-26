from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Menu Name")
    
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100, verbose_name="Title")
    url = models.CharField(max_length=200, blank=True, verbose_name="URL")
    named_url = models.CharField(max_length=100, blank=True, verbose_name="Named URL")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'
    
    def get_level(self):
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
