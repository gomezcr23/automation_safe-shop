import smtplib
import os
import datetime

from email.utils import formataddr
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS")
EMAIL_TRANSACTIONS = os.getenv("EMAIL_TRANSACTIONS")

DATE_FORMAT = "%Y-%m-%d %H:%M"
def send_email_password(user_email, token):
    if not user_email:
        raise ValueError("El correo electrónico no puede estar vacío")
    
    try:
        msg = EmailMessage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = f"SAFERUT {current_date}"
        msg["Subject"] = subject
        msg['From'] = formataddr(('App Saferut', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_email, user_email))

        reset_link = f"http://127.0.0.1:8000/auth/confirm-reset?token={token}"
        
        html_content = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="background-image: url('https://public-safered.s3.amazonaws.com/img/APP+SafeRut_Imagenes-01.png'); background-repeat: no-repeat; background-size: cover; padding-top: 40px; font-size: 17px; height: 530px; text-align: center;">
            <table align="center" style="width: 100%; max-width: 460px; background-color: white; border-radius: 30px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td align="center" style="padding: 25px;">
                        <img src="https://public-safered.s3.amazonaws.com/img/LOGO_SAFERUT-02.png" style="width: 230px;" alt="Logo" />
                        <p>Restablecimiento de contraseña, si usted no solicitó un restablecimiento de contraseña ignore este correo, si fue usted dele click en confirmar</p>
                        <br>
                        <a href="{reset_link}" style="background-color: #4b34c4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">Confirmar</a>
                    </td>
                </tr>
            </table>
            <br>
            <p style="padding: 25px; font-size: 12px; color: #4b34c4;">Por favor, no responda a este mensaje, ha sido enviado de forma automática. Si desea ponerse en contacto con nosotros para comentarnos alguna incidencia o mejora de este servicio, por favor, escríbanos a info@saferut.com.</p>
            <p style="font-size: 12px;"><strong>{current_date}</strong></p>
        </body>
        </html>
        """
        msg.set_content(html_content, subtype="html")

        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e
    if not user_email:
        raise ValueError("El correo electrónico no puede estar vacío")
    
    try:
        msg = EmailMessage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = f"SAFERUT {current_date}"
        msg["Subject"] = subject
        msg['From'] = formataddr(('App Saferut', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_email, user_email))
        
        html_content = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="background-image: url('https://public-safered.s3.amazonaws.com/img/APP+SafeRut_Imagenes-01.png'); background-repeat: no-repeat; background-size: cover; padding-top: 40px; font-size: 17px; height: 530px; text-align: center;">
            <table align="center" style="width: 100%; max-width: 460px; background-color: white; border-radius: 30px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td align="center" style="padding: 25px;">
                        <img src="https://public-safered.s3.amazonaws.com/img/LOGO_SAFERUT-02.png" style="width: 230px;" alt="Logo" />
                        <p>Restablecimiento de contraseña, si usted no solicitó un restablecimiento de contraseña ignore este correo, si fue usted dele click en confirmar</p>
                        <br>
                        <a href="http://127.0.0.1:8000/confirm-reset?email={user_email}" style="background-color: #4b34c4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">Confirmar</a>
                    </td>
                </tr>
            </table>
            <br>
            <p style="padding: 25px; font-size: 12px; color: #4b34c4;">Por favor, no responda a este mensaje, ha sido enviado de forma automática. Si desea ponerse en contacto con nosotros para comentarnos alguna incidencia o mejora de este servicio, por favor, escríbanos a info@saferut.com.</p>
            <p style="font-size: 12px;"><strong>{current_date}</strong></p>
        </body>
        </html>
        """
        msg.set_content(html_content, subtype="html")

        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

def send_email_with_attachments(user_email, user_name, files):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Reportes de transacciones, terceros e inventario"
        msg['From'] = formataddr(('Safe Shop', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_name, user_email))

        body = (
            "Adjunto encontrarás los reportes de transacciones, "
            "terceros e inventario correspondientes a las últimas 24 horas de Saferut.\n\n"
            "Esto es un correo automatizado."
        )
        msg.set_content(body)

        for file_name, file_content in files.items():
            msg.add_attachment(
                file_content.getvalue(),
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=file_name
            )

        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def send_email_registration_success( user_email, user_name ):
    try:
        current_date = datetime.datetime.now().strftime(DATE_FORMAT)
        
        # Create the email message
        msg = EmailMessage()
        msg["Subject"] = f"¡Bienvenido a Safe Shop, {user_name} -  {current_date}"
        msg['From'] = formataddr(('Safe Shop', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_name, user_email))
        html_content = f"""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333333;

                    padding: 40px;">
    <table align="center" style="width: 100%; max-width: 560px; border-radius: 30px; background-color: #ffffff;-webkit-box-shadow: 10px -1px 56px -20px rgba(0,0,0,0.74);
-moz-box-shadow: 10px -1px 56px -20px rgba(0,0,0,0.74);
box-shadow: 10px -1px 56px -20px rgba(0,0,0,0.74);">
        <tr>
            <td align="center" style="padding: 25px;">
                <img src="https://cdn.saferut.com/SafeShop/img/logo_.png" width="99" alt="Logo" />
                <p style="font-size: 16px"><strong>¡Bienvenido a SafeShop!🎉</strong></p>
                <br>
                <p>Nos alegra mucho que te hayas unido a nuestra comunidad. En SafeShop, nos comprometemos a ofrecerte una experiencia de compra segura, conveniente y personalizada.</p>
 
                <br><br>
                <p style="font-size: 11px; color: #0052cc;width: 100%;">Por favor, no responda a este mensaje, ha sido enviado de forma automática. Si desea ponerse en contacto con nosotros para comentarnos alguna incidencia o mejora de este servicio, por favor, escríbanos a info@saferut.com.</p>
                <p style="font-size: 12px;"><strong>{current_date}</strong></p>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        msg.set_content(html_content, subtype="html")

        # Enviar el mensaje
        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
    

def send_email_transaction_notification(user_email, user_name, user_lastname, user_phone, num_document, products):
    try:
        current_date = datetime.datetime.now().strftime(DATE_FORMAT)
        
        # Crear el mensaje de correo electrónico
        msg = EmailMessage()
        msg["Subject"] = f"Nueva Transacción Registrada - {current_date}"
        msg['From'] = formataddr(('Safe Shop', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr(('Comercial',EMAIL_TRANSACTIONS  ))
        
        products_html = ""
        for product in products:
            products_html += f"""
            <tr>
                <td>{product['name']}</td>
                <td>{product['price']}</td>
                <td>{product['descr']}</td>
            </tr>
            """
        
        html_content = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333333;
                    text-align: center;
                    padding: 40px;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #dddddd;
                }}
                th {{
                    background-color: #4b34c4;
                    color: white;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #4b34c4;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Nueva Transacción Registrada</h2>
                <p>Se ha registrado una nueva transacción con los siguientes detalles:</p>
                <table>
                    <tr>
                        <th>Documento</th>
                        <td>{num_document}</td>
                    </tr>
                    <tr>
                        <th>Nombre</th>
                        <td>{user_name}</td>
                    </tr>
                    <tr>
                        <th>Apellidos</th>
                        <td>{user_lastname}</td>
                    </tr>
                    <tr>
                        <th>Teléfono</th>
                        <td>{user_phone}</td>
                    </tr>
                    <tr>
                        <th>Correo Electrónico</th>
                        <td>{user_email}</td>
                    </tr>
                </table>
                <h3>Productos</h3>
                <table>
                    <tr>
                        <th>Nombre</th>
                        <th>Precio</th>
                        <th>Descripción</th>
                    </tr>
                    {products_html}
                </table>
                <p class="footer">Esto es un correo automatizado.</p>
                <p class="footer"><strong>{current_date}</strong></p>
            </div>
        </body>
        </html>
        """
        msg.set_content(html_content, subtype="html")

        # Enviar el mensaje
        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        print("Correo enviado exitosamente.")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
    



def send_email_purchase_notification(user_email, products):
    try:
        current_date = datetime.datetime.now().strftime(DATE_FORMAT)
        
        # Crear el mensaje de correo electrónico
        msg = EmailMessage()
        msg["Subject"] = f"Compra de Producto(s) Registrada - {current_date}"
        msg['From'] = formataddr(('Safe Shop', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_email, user_email))
        
        products_html = ""
        for product in products:
            products_html += f"""
            <tr>
                <td>{product['name']}</td>
                <td>{product['price']}</td>
                <td>{product['descr']}</td>
                <td>{product['purchase_date']}</td>
                <td>{product['subscription_end_date']}</td>
            </tr>
            """
        
        html_content = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333333;
                    text-align: center;
                    padding: 40px;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #dddddd;
                }}
                th {{
                    background-color: #4b34c4;
                    color: white;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #4b34c4;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Compra de Producto(s) Registrada</h2>
                <p>Se ha registrado una nueva compra con los siguientes detalles:</p>
                <h3>Productos</h3>
                <table>
                    <tr>
                        <th>Nombre</th>
                        <th>Precio</th>
                        <th>Descripción</th>
                        <th>Fecha de Compra</th>
                        <th>Fecha Fin de Suscripción</th>
                    </tr>
                    {products_html}
                </table>
                <p class="footer">Por favor, no responda a este mensaje, ha sido enviado de forma automática. Si desea ponerse en contacto con nosotros para comentarnos alguna incidencia o mejora de este servicio, por favor, escríbanos a info@saferut.com.</p>
                <p class="footer"><strong>{current_date}</strong></p>
            </div>
        </body>
        </html>
        """
        msg.set_content(html_content, subtype="html")

        # Enviar el mensaje
        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        print("Correo enviado exitosamente.")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False