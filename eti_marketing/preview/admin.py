from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . import models


class SlideWaypointInline(admin.StackedInline):
    model = models.SlideWaypoint


@admin.register(models.Slide)
class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    view_on_site = True
    save_as = True

    fields = ('title', 'caption', 'screenshot')
    inlines = (SlideWaypointInline,)
