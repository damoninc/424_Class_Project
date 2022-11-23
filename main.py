import email
import mailbox
from email.message import EmailMessage
import re
import hashlib


def mailhasher(mb):
    """
    Hashes emails given by the mailbox MIME format.
    :param mb: Some mbox file
    :return: Nothing
    """
    with open("payloadhashes.txt", "w") as plh, open("urls.txt", "w") as urls:

        for key in mb.iterkeys():  # Iterating through the .mbox
            content = mb.get_message(key)  # Raw mailbox payload
            msg = EmailMessage()
            msg.set_content(content)  # Switching from mailbox to Email message object

            new_msg = email.message_from_string(str(msg))  # Message Object
            for part in new_msg.walk():  # Iterating through the emails
                if part.get_content_type() == 'text/plain':  # Checks to see if the email is plain text
                    message = re.sub("\n", "", part.get_payload())
                    encoded_message = message.encode()  # Encodes the email
                    plh.write(hashlib.sha256(encoded_message).hexdigest() + "\n")  # Writes the hashed email to txt
                    for url in urlgrabber(message):  # Writes any urls within the email to text
                        urls.write(url+"\n")

def urlgrabber(mystring, a_list = []):
    """
    Helper function for the main mail hasher but it grabs urls out of a string.
    :param mystring: The body/payload of the email.
    :param a_list: List of the urls
    :return: Nothing
    """
    try:
        if (re.search("(?P<url>https?://[^\s|>]+)", mystring).group("url")) == False:
            return a_list

        elif (re.search("(?P<url>https?://[^\s|>]+)", mystring).group("url")):
            a_list.append((re.search("(?P<url>https?://[^\s|>]+)", mystring).group("url")))
            new_string = re.search("(?P<url>https?://[^\s|>]+)", mystring).group("url")
            return urlgrabber(mystring.replace(new_string, "x"), a_list)
    except AttributeError:
        return a_list

#mailhasher(mailbox.mbox("Spam.mbox"))








