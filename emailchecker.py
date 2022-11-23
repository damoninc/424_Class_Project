import email
import mailbox
from email.message import EmailMessage
import re
import hashlib


def mail_checker(mb):
    """
    Checks and compares a given mailbox to a set of blacklisted email hashes, urls and checks for lack of unsubs
    :param mb: Some mailbox in in MIME format
    :return: Prints Spam or Not Spam
    """
    with open("payloadhashes.txt", "r") as plh, open("urls.txt", "r") as urls:

        for key in mb.iterkeys():  # Iterating through the .mbox
            content = mb.get_message(key)  # Raw mailbox payload
            msg = EmailMessage()
            msg.set_content(content)  # Switching from mailbox to Email message object

            new_msg = email.message_from_string(str(msg))  # Turns content from string into a Message obj.
            for part in new_msg.walk():  # Iterates through the email
                spam_checker = False  # initiating a flag
                if part.get_content_type() == 'text/plain':
                    message = re.sub("\n", "", part.get_payload())
                    encoded_message = message.encode()
                    if hashlib.sha256(encoded_message).hexdigest() + "\n" in plh:  # Hash comparison
                        spam_checker = True
                    for url in urlchecker(message):  # URL comparison
                        if url + "\n" in urls:
                            spam_checker = True
                    if unsubscribe(message):  # Unsub checker
                        spam_checker = True
                    # Based on Flag results, prints Spam or Not spam
                    if spam_checker:
                        print("Spam")
                    else:
                        print("Not Spam")


def urlchecker(mystring, a_list = []):
    """
    URL Checker helper function for mailchecker()
    :param mystring: Takes in the given email string
    :param a_list: List of urls
    :return: List of urls
    """
    try:
        if (re.search("(?P<url>https?://[^\s]+)", mystring).group("url")) == False:  # Checks for lack of url
            return a_list

        elif (re.search("(?P<url>https?://[^\s]+)", mystring).group("url")):  # Checks for url and recursively 
            a_list.append((re.search("(?P<url>https?://[^\s]+)", mystring).group("url")))
            new_string = re.search("(?P<url>https?://[^\s]+)", mystring).group("url")
            return urlchecker(mystring.replace(new_string, "x"), a_list)
    except AttributeError:
        return a_list

def unsubscribe(message):
    """
    Takes in a message and checks for unsubscribes
    :param message: Payload message
    :return: Boolean value
    """
    if (re.search(r"Unsubscribe | unsubscribe", message)):
        return True
    else:
        return False


mail_checker(mailbox.mbox("Mailsample.mbox"))