from django.shortcuts import render, get_object_or_404, redirect
from .models import Testplan, Checklist, TestPlanTemplate
# (other imports remain as needed)

def testplan_detail(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    checklist = Checklist.objects.filter(reservation=testplan.reservation).first()
    # Retrieve the TestPlanTemplate associated with this Testplan.
    # (This example assumes that when creating a testplan, a TestPlanTemplate was created with the same name.)
    template = TestPlanTemplate.objects.filter(name=testplan.name).first()
    steps = template.steps.all() if template else []
    return render(request, 'testplans/testplan_details.html', {
        'testplan': testplan,
        'checklist': checklist,
        'reservation': testplan.reservation,
        'steps': steps,
    })
