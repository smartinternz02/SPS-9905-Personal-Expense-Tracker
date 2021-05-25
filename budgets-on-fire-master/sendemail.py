import smtplib

from email.message import EmailMessage
def forgotemail(TEXT,tomail):
    msg = EmailMessage()
    msg['Subject'] = 'Forgot your Password'
    msg['From'] = 'budgetbuddy.in@gmail.com'
    msg['To'] = tomail
    msg.set_content('')
    msg.add_alternative(TEXT,subtype='html')


    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('budgetbuddy.in@gmail.com','Candy@69')
        smtp.send_message(msg)


def sendgrid(TEXT,email):
    msg = EmailMessage()
    msg['Subject'] = 'Alert!! Monthly Limit Exceeded'
    msg['From'] = 'budgetbuddy.in@gmail.com'
    msg['To'] = email
    msg.set_content('')
    msg.add_alternative(TEXT,subtype='html')


    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('budgetbuddy.in@gmail.com','Candy@69')
        smtp.send_message(msg)

   
