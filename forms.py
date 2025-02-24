from django import forms
from .models import Checklist, Testplan, TemplateStep

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = [
            'support_assistance', 'support_workcenter', 'safety_risks', 'safety_overrides',
            'software_changes', 'software_changes_stay', 'software_devpatch', 'software_dolly_devbench',
            'hardware_recipes', 'hardware_changes', 'hardware_changes_stay', 'hardware_arrangement',
            'config_hw_requirements', 'config_sw_requirements', 'tools_dev_reticles', 'tools_customer_reticles',
            'dont_forget_recovery_time'
        ]
        labels = {
            'support_assistance': 'What kind of assistance do you require from SI-PE?',
            'support_workcenter': 'Is Workcenter / FLS / FASY / VIS support needed? Make sure the support is arranged.',
            'safety_risks': 'Are there specific risks associated to this claim?',
            'safety_overrides': 'Are Safety overrides involved? Who will arrange it?',
            'software_changes': 'Will there be SW changes to the system for this test claim?',
            'software_changes_stay': 'Will the SW changes stay on the system after the UID is finished?',
            'software_devpatch': 'Do you plan to test with a devpatch, test package or manual firmware?',
            'software_dolly_devbench': 'Have you verified if everything functions as expected on a Dolly or Devbench?',
            'hardware_recipes': 'Have you uploaded your recipes / queues / clipfiles etc. to the correct disk?',
            'hardware_changes': 'Will there be HW changes to the system for this test claim?',
            'hardware_changes_stay': 'Will the HW changes stay on the system after the UID is finished?',
            'hardware_arrangement': 'Who will arrange the new/additional HW needed for this test claim and how will it be delivered to the cabin?',
            'config_hw_requirements': 'Specify what HW config requirements you need at the system?',
            'config_sw_requirements': 'Specify what SW config requirements you need at the system?',
            'tools_dev_reticles': 'Development Reticles needed? (Reticle Workcenter)',
            'tools_customer_reticles': 'Customer reticle(s) needed? (Reticle Workcenter)',
            'dont_forget_recovery_time': 'If your test will change the setup-state or stability of the system, have you already considered Recovery-time on your test block?',
        }
        widgets = {
            'support_assistance': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'support_workcenter': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'safety_risks': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'safety_overrides': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'software_changes': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'software_changes_stay': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'software_devpatch': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'software_dolly_devbench': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'hardware_recipes': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'hardware_changes': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'hardware_changes_stay': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'hardware_arrangement': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'config_hw_requirements': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'config_sw_requirements': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'tools_dev_reticles': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'tools_customer_reticles': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'dont_forget_recovery_time': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }

class TestplanForm(forms.ModelForm):
    class Meta:
        model = Testplan
        fields = ['name', 'description']

class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(choices=[
        ('approved', 'Approved'),
        ('rework', 'Rework'),
        ('declined', 'Declined')
    ])

class TestPlanStepForm(forms.ModelForm):
    class Meta:
        model = TemplateStep
        fields = ['step_order', 'section', 'step', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments']
        widgets = {
            'step_order': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'step': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'procedure': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1 resize-y', 'rows': 1}),
            'day_time_duration': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'nq_duration': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'executor': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'comments': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1 resize-y', 'rows': 1}),
            'section': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].required = False
        self.fields['step_order'].required = False
