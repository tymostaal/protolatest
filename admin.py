from django.contrib import admin
from .models import Checklist, Testplan, TestPlanTemplate, TemplateStep, PredefinedStep

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'support_assistance', 'support_workcenter', 'safety_risks')
    search_fields = ('reservation__name', 'support_assistance', 'support_workcenter')

class TestplanAdmin(admin.ModelAdmin):
    list_display = ('name', 'reservation', 'created_at', 'updated_at', 'ste_status', 'pce_hw_status', 'pce_sw_status', 'po_status', 'pe_status')
    search_fields = ('name', 'reservation__name')
    list_filter = ('ste_status', 'pce_hw_status', 'pce_sw_status', 'po_status', 'pe_status')

class TestPlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'folder', 'created_at')
    search_fields = ('name',)

class TemplateStepAdmin(admin.ModelAdmin):
    list_display = ('template', 'step_order', 'section', 'step')
    search_fields = ('template__name', 'step')
    list_filter = ('section',)

class PredefinedStepAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'folder')
    search_fields = ('name',)
    list_filter = ('section',)

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Testplan, TestplanAdmin)
admin.site.register(TestPlanTemplate, TestPlanTemplateAdmin)
admin.site.register(TemplateStep, TemplateStepAdmin)
admin.site.register(PredefinedStep, PredefinedStepAdmin)