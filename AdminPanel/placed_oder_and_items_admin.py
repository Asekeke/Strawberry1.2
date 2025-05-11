from django.contrib import admin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from products.models import *

class PlacedOderItemTabularAdmin(admin.TabularInline):
    model = PlacedeOderItem
    extra = 0

class OderManagementAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'sub_total_price', 'paid', 'user']
    list_editable = ['paid']
    list_filter = ['status', 'placed_date']
    inlines = (PlacedOderItemTabularAdmin,)

    def save_model(self, request, obj, form, change):
        # Если заказ отгружен — переносим его в CompletedOder
        if change and obj.status == 'Order Shipped':
            completed = CompletedOder.objects.create(
                user=obj.user,
                shipping_address=obj.shipping_address,
                sub_total_price=obj.sub_total_price,
                paid=obj.paid,
                status='Order Shipped',
                oder_number=obj.order_number
            )
            items = obj.order_items.all()
            CompletedOderItems.objects.bulk_create([
                CompletedOderItems(
                    completed_oder=completed,
                    product=i.product,
                    quantity=i.quantity,
                    total_price=i.total_price
                ) for i in items
            ])
            items.delete()
            obj.delete()
            return redirect('/custom-admin/products/placedoder/')

        obj.save()
        super().save_model(request, obj, form, change)

        # Сохраняем элементы заказа и пересчитываем сумму
        formset_class = inlineformset_factory(PlacedOder, PlacedeOderItem, fields=('product', 'quantity'))
        formset = formset_class(request.POST, instance=obj)
        if formset.is_valid():
            formset.save()
            obj.sub_total_price = sum(i.total_price for i in obj.order_items.all())
            obj.save()

