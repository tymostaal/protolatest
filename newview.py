from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from .models import Testplan, Checklist, TemplateStep, TestPlanTemplate
from .forms import TestplanForm, ChecklistForm, ReviewForm, TestPlanStepForm
from reservations.models import Reservation, ReservationStatus

def hello_view(request):
    return render(request, 'testplans/hello.html')

def create_testplan(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    existing_testplan = reservation.testplans.first()
    if existing_testplan:
        return redirect('testplan_detail', testplan_id=existing_testplan.id)  # Redirect to existing testplan detail page

    if request.method == 'POST':
        form = TestplanForm(request.POST)
        if form.is_valid():
            testplan = form.save(commit=False)
            testplan.reservation = reservation
            testplan.save()
            print("Testplan created, calling add_test_plan")
            reservation.add_test_plan()  # Update status or related actions
            return redirect('create_testplan_steps', testplan_id=testplan.id)
        else:
            print("Form is not valid:", form.errors)
    else:
        form = TestplanForm()
    return render(request, 'testplans/create_testplan.html', {'form': form, 'reservation': reservation})

def testplan_detail(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    checklist = Checklist.objects.filter(reservation=testplan.reservation).first()
    return render(request, 'testplans/testplan_details.html', {'testplan': testplan, 'checklist': checklist})

def review_test_plan(request, test_plan_id):
    test_plan = get_object_or_404(Testplan, id=test_plan_id)
    reservation = test_plan.reservation
    user_groups = request.user.groups.values_list('name', flat=True)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            comment = form.cleaned_data['comment']
            
            if 'STE' in user_groups:
                test_plan.ste_status = status
            elif 'PCE HW' in user_groups:
                test_plan.pce_hw_status = status
            elif 'PCE SW' in user_groups:
                test_plan.pce_sw_status = status
            elif 'PO' in user_groups:
                test_plan.po_status = status
            elif 'PE' in user_groups:
                test_plan.pe_status = status
            
            test_plan.save()

            # Check if all reviews are approved and update reservation status if needed
            if test_plan.all_reviews_approved():
                test_plan.reservation.status = ReservationStatus.TRANSFER_TO_PROTO
                test_plan.reservation.save()

            return redirect('testplan_detail', testplan_id=test_plan.id)
    else:
        form = ReviewForm()
    
    return render(request, 'testplans/review_test_plan.html', {
        'form': form,
        'test_plan': test_plan,
        'reservation': reservation
    })

# Wizard for the checklist step
FORMS = [
    ("checklist", ChecklistForm),
]

TEMPLATES = {
    "checklist": "testplans/checklist_form.html",
}

class TestplanWizard(SessionWizardView):
    form_list = FORMS
    template_name = "testplans/form_wizard.html"

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        reservation_id = self.kwargs.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)
        context['reservation'] = reservation
        return context

    def get_form_instance(self, step):
        if step == 'checklist':
            reservation_id = self.kwargs['reservation_id']
            reservation = Reservation.objects.get(id=reservation_id)
            return Checklist(reservation=reservation)
        return super().get_form_instance(step)

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        reservation_id = self.kwargs['reservation_id']
        reservation = Reservation.objects.get(id=reservation_id)

        # Save checklist responses
        checklist = Checklist(
            reservation=reservation,
            support_assistance=form_data[0]['support_assistance'],
            support_workcenter=form_data[0]['support_workcenter'],
            safety_risks=form_data[0]['safety_risks'],
            safety_overrides=form_data[0]['safety_overrides'],
            software_changes=form_data[0]['software_changes'],
            software_changes_stay=form_data[0]['software_changes_stay'],
            software_devpatch=form_data[0]['software_devpatch'],
            software_dolly_devbench=form_data[0]['software_dolly_devbench'],
            hardware_recipes=form_data[0]['hardware_recipes'],
            hardware_changes=form_data[0]['hardware_changes'],
            hardware_changes_stay=form_data[0]['hardware_changes_stay'],
            hardware_arrangement=form_data[0]['hardware_arrangement'],
            config_hw_requirements=form_data[0]['config_hw_requirements'],
            config_sw_requirements=form_data[0]['config_sw_requirements'],
            tools_dev_reticles=form_data[0]['tools_dev_reticles'],
            tools_customer_reticles=form_data[0]['tools_customer_reticles'],
            dont_forget_recovery_time=form_data[0]['dont_forget_recovery_time'],
        )
        checklist.save()

        # Create a Testplan instance for this reservation
        testplan = Testplan.objects.create(
            name=f"Testplan for {reservation}",
            description="Auto-generated from checklist responses",
            reservation=reservation
        )
        # Optionally update reservation status
        reservation.add_test_plan()

        print("Redirecting to create_testplan_steps with testplan id:", testplan.id)
        return redirect('create_testplan_steps', testplan_id=testplan.id)

# Updated view for the drag-and-drop steps interface
def create_testplan_steps(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    # Get or create a corresponding TestPlanTemplate for this testplan
    template, created = TestPlanTemplate.objects.get_or_create(
        name=testplan.name,
        defaults={'description': testplan.description}
    )
    
    PreparationFormSet = modelformset_factory(
        TemplateStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    ExecutionFormSet = modelformset_factory(
        TemplateStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    WrapupFormSet = modelformset_factory(
        TemplateStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        prep_formset = PreparationFormSet(request.POST, queryset=TemplateStep.objects.none(), prefix='prep')
        exec_formset = ExecutionFormSet(request.POST, queryset=TemplateStep.objects.none(), prefix='exec')
        wrap_formset = WrapupFormSet(request.POST, queryset=TemplateStep.objects.none(), prefix='wrap')
        
        if prep_formset.is_valid() and exec_formset.is_valid() and wrap_formset.is_valid():
            for form in prep_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'preparation'
                    step_instance.template = template  # Associate with the template
                    step_instance.save()
            
            for form in exec_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'execution'
                    step_instance.template = template  # Associate with the template
                    step_instance.save()
            
            for form in wrap_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'wrapup'
                    step_instance.template = template  # Associate with the template
                    step_instance.save()
            
            return redirect('testplan_detail', testplan_id=testplan.id)
    else:
        prep_formset = PreparationFormSet(queryset=TemplateStep.objects.none(), prefix='prep')
        exec_formset = ExecutionFormSet(queryset=TemplateStep.objects.none(), prefix='exec')
        wrap_formset = WrapupFormSet(queryset=TemplateStep.objects.none(), prefix='wrap')
    
    context = {
        'testplan': testplan,
        'prep_formset': prep_formset,
        'exec_formset': exec_formset,
        'wrap_formset': wrapup_formset,
    }
    return render(request, 'testplans/testplan_form.html', context)
