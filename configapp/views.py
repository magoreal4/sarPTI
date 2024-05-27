from .models import PolicyDocument, TermsConditions
from django.shortcuts import render
 
def policy_view(request):
    policy = PolicyDocument.objects.first()
    return render(request, 'policy_template.html', {'policy': policy})

def terms_view(request):
    terms = TermsConditions.objects.first()
    return render(request, 'terms_template.html', {'terms': terms})
