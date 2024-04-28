# send_test_email.py

from django.core.mail import send_mail, BadHeaderError
from django.core.management.base import BaseCommand
from smtplib import SMTPException

class Command(BaseCommand):
    help = 'Sends a test email.'

    def handle(self, *args, **options):
        try:
            send_mail(
                'Hello from Django',
                'This is a test email sent from Django application.',
                'admin@btspti.com',
                ['magoreal4@gmail.com'],  # Asegúrate que esta dirección es correcta y puede recibir correos
                fail_silently=False,  # Cambiado a False para ver errores
            )
            self.stdout.write(self.style.SUCCESS('Successfully sent email.'))
        except (SMTPException, BadHeaderError) as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email. Error: {e}'))
