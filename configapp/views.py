from .models import PolicyDocument, TermsConditions, ApkFile
from django.shortcuts import render
 
def policy_view(request):
    policy = PolicyDocument.objects.first()
    return render(request, 'policy_template.html', {'policy': policy})

def terms_view(request):
    terms = TermsConditions.objects.first()
    return render(request, 'terms_template.html', {'terms': terms})

def file_list(request):
    files = ApkFile.objects.all()
    return render(request, 'file_list.html', {'files': files})