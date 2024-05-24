
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import SupportQueryForm
from configapp.models import SiteConfiguration

def support_view(request):
    if request.method == 'POST':
        form = SupportQueryForm(request.POST)        
        if form.is_valid():
            support_query = form.save()

            # Obtener los destinatarios desde SiteConfiguration
            site_config = SiteConfiguration.objects.first()  # Asumiendo que solo hay una configuración
            if site_config and site_config.recipients:
                recipient_list = [email.strip() for email in site_config.recipients.split(',')]
            else:
                recipient_list = []

            # Datos del formulario para el correo electrónico
            subject = 'Nueva consulta de soporte'
            message = f'Has recibido una nueva consulta de soporte:\n\n' \
                      f'Nombre: {support_query.name}\n' \
                      f'Correo Electrónico: {support_query.email}\n' \
                      f'Mensaje: {support_query.message}'
            from_email = 'admin@btspti.com'

            # Enviar correo electrónico solo si hay destinatarios
            if recipient_list:
                send_mail(subject, message, from_email, recipient_list)

            return redirect('support:support_success')
    else:
        form = SupportQueryForm()
    return render(request, 'support_form.html', {'form': form})

def support_success(request):
    return render(request, 'support_success.html')
