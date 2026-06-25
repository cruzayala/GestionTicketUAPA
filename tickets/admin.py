from django.contrib import admin

from .models import Ticket, TicketEvent


class TicketEventInline(admin.TabularInline):
    model = TicketEvent
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("number", "subject", "full_name", "priority", "status", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("number", "subject", "full_name", "email")
    inlines = [TicketEventInline]


@admin.register(TicketEvent)
class TicketEventAdmin(admin.ModelAdmin):
    list_display = ("ticket", "title", "created_at")
    search_fields = ("ticket__number", "title")
