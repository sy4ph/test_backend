from django.core.management.base import BaseCommand
from tree_menu.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Populate database with sample menu data'

    def handle(self, *args, **options):
        MenuItem.objects.all().delete()
        Menu.objects.all().delete()
        
        main_menu = Menu.objects.create(name='main_menu')
        
        home = MenuItem.objects.create(
            menu=main_menu, title='Home', url='/', order=1)
        
        about = MenuItem.objects.create(
            menu=main_menu, title='About', url='/about/', order=2)
        
        services = MenuItem.objects.create(
            menu=main_menu, title='Services', url='/services/', order=3)
        
        web_dev = MenuItem.objects.create(
            menu=main_menu, title='Web Development', 
            url='/services/web-development/', parent=services, order=1)
        
        mobile_dev = MenuItem.objects.create(
            menu=main_menu, title='Mobile Development',
            url='/services/mobile-development/', parent=services, order=2)
        
        ios_dev = MenuItem.objects.create(
            menu=main_menu, title='iOS Development',
            url='/services/mobile-development/ios/', parent=mobile_dev, order=1)
        
        android_dev = MenuItem.objects.create(
            menu=main_menu, title='Android Development',
            url='/services/mobile-development/android/', parent=mobile_dev, order=2)
        
        products = MenuItem.objects.create(
            menu=main_menu, title='Products', url='/products/', order=4)
        
        product1 = MenuItem.objects.create(
            menu=main_menu, title='Product 1', url='/products/1/', parent=products, order=1)
        
        product2 = MenuItem.objects.create(
            menu=main_menu, title='Product 2', url='/products/2/', parent=products, order=2)
        
        contact = MenuItem.objects.create(
            menu=main_menu, title='Contact', url='/contact/', order=5)
        
        secondary_menu = Menu.objects.create(name='secondary_menu')
        
        help_item = MenuItem.objects.create(
            menu=secondary_menu, title='Help', url='/help/', order=1)
        
        faq = MenuItem.objects.create(
            menu=secondary_menu, title='FAQ', 
            url='/faq/', parent=help_item, order=1)
        
        docs = MenuItem.objects.create(
            menu=secondary_menu, title='Documentation',
            url='/docs/', parent=help_item, order=2)
        
        support = MenuItem.objects.create(
            menu=secondary_menu, title='Support', url='/support/', order=2)
        
        self.stdout.write(self.style.SUCCESS('Sample menu data created successfully'))
