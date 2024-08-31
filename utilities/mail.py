import time
import imaplib
import email

from email.header import decode_header


def decode_body(message):
    email_body = ""
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_body = part.get_payload(decode=True).decode()  # decode email body
                break
    else:
        email_body = message.get_payload(decode=True).decode()
    return email_body


def decode_subject(subject):
    decoded_parts = decode_header(subject)
    return ''.join([str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0] for t in decoded_parts])


def check_email_arrived(username, password, subject, recipient_email, timeout=30, interval=5):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")

    end_time = time.time() + timeout

    while time.time() < end_time:
        mail.recent()
        status, messages = mail.search(None, 'UNSEEN')
        if status == "OK":
            for num in messages[0].split():
                status, msg_data = mail.fetch(num, "(RFC822)")
                if status == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    msg_subject = decode_subject(msg["subject"])
                    msg_to = msg["to"]
                    if subject in msg_subject and recipient_email in msg_to:
                        return msg

        time.sleep(interval)

    return None
