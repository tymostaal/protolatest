from django.db import models
from reservations.models import Reservation

class Checklist(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='checklists')
    support_assistance = models.TextField()
    support_workcenter = models.TextField()
    safety_risks = models.TextField()
    safety_overrides = models.TextField()
    software_changes = models.TextField()
    software_changes_stay = models.TextField()
    software_devpatch = models.TextField()
    software_dolly_devbench = models.TextField()
    hardware_recipes = models.TextField()
    hardware_changes = models.TextField()
    hardware_changes_stay = models.TextField()
    hardware_arrangement = models.TextField()
    config_hw_requirements = models.TextField()
    config_sw_requirements = models.TextField()
    tools_dev_reticles = models.TextField()
    tools_customer_reticles = models.TextField()
    dont_forget_recovery_time = models.TextField()

    def __str__(self):
        return f"Checklist for {self.reservation}"

class Testplan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='testplans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ste_status = models.CharField(max_length=10, default='REVW')
    pce_hw_status = models.CharField(max_length=10, default='REVW')
    pce_sw_status = models.CharField(max_length=10, default='REVW')
    po_status = models.CharField(max_length=10, default='REVW')
    pe_status = models.CharField(max_length=10, default='REVW')

    def __str__(self):
        return self.name
    
    def all_reviews_approved(self):
        return all([
            self.ste_status == 'approved',
            self.pce_hw_status == 'approved',
            self.pce_sw_status == 'approved',
            self.po_status == 'approved',
            self.pe_status == 'approved'
        ])

class TestPlanTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TemplateStep(models.Model):
    SECTION_CHOICES = (
        ('preparation', 'Preparation Steps'),
        ('execution', 'Execution Steps'),
        ('wrapup', 'Wrap-Up Steps'),
    )
    template = models.ForeignKey(TestPlanTemplate, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField(default=0)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    step = models.CharField(max_length=255)
    procedure = models.TextField(blank=True)
    day_time_duration = models.CharField(max_length=100, blank=True)
    nq_duration = models.CharField(max_length=100, blank=True)
    executor = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['section', 'step_order']
    
    def __str__(self):
        return f"{self.template.name} - {self.get_section_display()} - {self.step}"

class PredefinedStep(models.Model):
    CATEGORY_CHOICES = (
        ('preparation', 'Preparation Steps'),
        ('execution', 'Execution Steps'),
        ('wrapup', 'Wrap-Up Steps'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=255, blank=True, default="")
    section = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    procedure = models.TextField(blank=True)
    day_time_duration = models.CharField(max_length=100, blank=True)
    nq_duration = models.CharField(max_length=100, blank=True)
    executor = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return self.name