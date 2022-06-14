def send_mail_to_reciever(sender_mail_id, sender_app_password, receiver_mail_id, receiver_name):
    import smtplib
    import sys

    smtp_object  =smtplib.SMTP('smtp.gmail.com', 587)
    connection_status, _ = smtp_object.ehlo()
   
    if connection_status != 250:
        print('Connection not established! Please check your internet connection!')
        sys.exit(0)
        
    connection_status, _ = smtp_object.starttls()
    if connection_status != 220:
        print('Something unexpected error has been occured!')
        sys.exit(0)


    smtp_object.login(sender_mail_id, sender_app_password)
    subject = 'Attendance Marked Successfully'
    message = f'''
    Hi {receiver_name.split(' ')[0]},
    Your attendance has been marked successfully by our system.
    Have a good day!

    Thanks & Regards
    Automated Attendance Marking System
    '''
    msg = "Subject: " + subject + '\n' + message
    smtp_object.sendmail(sender_mail_id, receiver_mail_id, msg)
    smtp_object.quit()
    
