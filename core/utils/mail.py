from django.core.mail import EmailMultiAlternatives, get_connection


def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    bcc=None,
    connection=None,
    html_message=None,
):
    """
    Wrapper to send email with bcc option.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, connection=connection, bcc=bcc
    )
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()
