from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Slide


@admin.register(Slide)
class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    view_on_site = True
    save_as = True

    fields = ('title', 'caption', 'screenshot')
