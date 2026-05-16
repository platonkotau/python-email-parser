from dotenv import load_dotenv, find_dotenv
import os
import imaplib
import email
from groq import Groq


def categ_ai(subject, sender):

    content = f"""Categorize this email into ONE of these categories:
                - invoice: payment, receipt, order, bill
                - code: verification code, OTP, confirmation code, security code  
                - spam: marketing, promotion, advertisement, newsletter
                - security: security alert, recent changes, 
                - other: everything else
                - personal: if sender is some human not a company

                and take care of sender if sender is some company like Steam, Supabase, Facebook you need to check it twice before you categorize email,
                because there is some bad people who can send me something with security subject but it can be not security so you need to check is sender is company
                or just human take infomration about companies from inetrnet 


                Reply with ONE word only: invoice, code, spam, security, personal or other.

                Subject: {subject}
                From: {sender}"""

    client = Groq(api_key=os.getenv("GROQ_KEY"))

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": content}
    ])

    return response.choices[0].message.content

load_dotenv()




user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")



imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(user, password)
imap.select("INBOX")

status, messages = imap.search(None, "ALL")
last_id = messages[0].split()
last_message = last_id[-1]
status, data = imap.fetch(last_message, "(RFC822)")
raw_msg = data[0][1]
msg = email.message_from_bytes(raw_msg)

print(msg["Subject"])
print(msg["From"])
print(msg["Date"])

print(categ_ai(msg["Subject"], msg["From"]))

