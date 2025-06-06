import logging
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import Logger
from hoa_insights_surpriseaz import my_secrets

email_reciever: list[str] = my_secrets.email_to
email_sender: str = my_secrets.postfix_mail_from
email_server = my_secrets.postfix_mailhost
email_user = my_secrets.postfix_user
email_password = my_secrets.postfix_password


def send_mail(subject: str, attachment_path: str = None) -> None:
    """
    Function takes a subject and optional file attachment path as strings.
    Sends email to contacts.
    """
    logger: Logger = logging.getLogger(__name__)

    msg: MIMEMultipart = MIMEMultipart("alternative")
    msg["Subject"] = f"{subject}"
    msg["From"] = email_sender
    msg["To"] = email_reciever[0]

    if attachment_path:
        html_attachments: str = """\
          <html>
            <body>
              <p><b>Python HOA Insights Report Mailer</b></p>
              <br>
              <p>Please find the bi-monthly community changes report attached.</p>
              <br>
              <p>Visit below for more information</p>
              <a href="https://hoa.tascs.test">TASCS HOA</a>       
            </body>
          </html>
          """
        with open(attachment_path, "rb") as attachment:
            html: MIMEText = MIMEText(html_attachments, "html")
            part_attachments: MIMEBase = MIMEBase("application", "octet-stream")
            part_attachments.set_payload(attachment.read())
            encoders.encode_base64(part_attachments)
            part_attachments.add_header(
                "Content-Disposition", "attachment", filename=attachment_path
            )
            msg.attach(part_attachments)
            msg.attach(html)

    else:
        html_basic: str = """\
            <html>
              <body>
                <p><b>Python HOA Insights Mailer</b>
                <br>
                   Visit <a href="https://hoa.tascs.test">TASCS HOA</a> 
                   for more information.
                </p>
              </body>
            </html>
            """
        part_basic: MIMEText = MIMEText(html_basic, "html")
        msg.attach(part_basic)

    # WORKS WITH NO AUTH ON 25
    # with smtplib.SMTP(my_secrets.postfix_mailhost, 25) as server:
    #     try:
    #         server.sendmail(email_sender, email_reciever, msg.as_string())

    #     except smtplib.SMTPException as e:
    #         logger.exception(str(e))

    # TODO USE SASL WITH RELAYS
    # TESTING W/SASL AUTH. IF AUTH FAILS STILL SENDS smtp_sasl_auth_enable = yes
    #  fatal: specify a password table via the `smtp_sasl_password_maps' configuration parameter. DONE
    # https://serverfault.com/questions/698854/postfix-fatal-specify-a-password-table-via-the-smtp-sasl-password-maps-config
    # https://www.lunanode.com/guides/postfix_smtp_secure
    # warning: SASL authentication failure: No worthy mechs found. May need to install more packages
    # smtp_sasl_auth_enable is still ENABLED, ignoring msgs
    # KEEP AN EYE ON SEEMS FINE AFTER change to sasl_passwd file (added [] to mail host)

    try:
        with smtplib.SMTP(
            email_server, 587, local_hostname="debian.tascs.test"
        ) as server:
            server.ehlo()
            server.starttls()
            try:
                server.login(email_user, email_password)
            except smtplib.SMTPAuthenticationError as login_err:
                logger.error(f"\t{login_err}")

            server.sendmail(email_sender, email_reciever, msg.as_string())
            logger.info("\temail sent")

    except smtplib.SMTPException as err:
        if "Connection refused" in err.msg:
            logger.error(f"\tCheck Email Server {err.msg}")
            print(f"Check Email Server {err.msg}")

    # #################################### SSL TESTING
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)   # ssl.create_default_context
    # context.set_ciphers('TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384')        #("TLS_RSA_WITH_AES_128_CBC_SHA256")     # ("TLS_DHE_RSA_WITH_AES_128_GCM_SHA256")
    # context.hostname_checks_common_name = False
    # context.check_hostname = False
    # context.verify_mode = ssl.CERT_NONE
    # ser_cert = ssl.get_server_certificate(my_secrets.exchange_mailhost, 25)


#     context.load_default_certs()
#     ca = context.get_ca_certs()
#     c = context.get_ciphers()
#     ciphers = list({x['name'] for x in c})
#     # print(ciphers)
#     # print(ca)
#     for c in ca:
#         sub = c.get('subject')
#         org = sub[1]
#         for o in org:
#             for p in o:
#                 print(p, type(p))
#         # for d in c:
#         #     print(d)
#         #     print(type(d))
#     try:
#         with smtplib.SMTP_SSL(my_secrets.exchange_mailhost, 587, context=context) as server:
#             server.login(my_secrets.exchange_user, my_secrets.exchange_password)  # NTLM issue? wrong version issue .997?
#             server.ehlo("tascslt")
#             server.starttls()
#             server.sendmail(my_secrets.mail_from, receiver_email, msg.as_string())
#
#     except smtplib.SMTPException as e:
#         print("SMTPERROR",e)
#     except ssl.SSLError as e:
#         print("SSLError", str(e))
#     except ssl.ALERT_DESCRIPTION_HANDSHAKE_FAILURE as e:
#         print(e)
#     except ssl.SSLCertVerificationError as e:
#         print(e)
#
# send_mail("hello, NON TLS test to rpi4 on port 25. Shows no date!?")
if __name__ == "__main__":
    send_mail("testing w/Attachment", "../output/csv/surpriseaz-hoa-management.csv")
