import re
myString = "Facebook <https://link.square-enix-games.com/click/29301660.1755448/aHR0cHM=6Ly93d3cuZmFjZWJvb2suY29tL1NxdWFyZUVuaXgvP3NhaWx0aHJ1X3ZhcnNbcm91bmR1cF9jbG=lja109MQ/5e4d4c4897a21435d12b28b5C261c5dda> Twitter <https://link.square-en="

myString1 = "facebook"



def urlgrabber(mystring, a_list = []):
    try:
        if (re.search("(?P<url>https?://[^\s]+)", mystring).group("url")) == False:
            return a_list

        elif (re.search("(?P<url>https?://[^\s]+)", mystring).group("url")):
            a_list.append((re.search("(?P<url>https?://[^\s]+)", mystring).group("url")))
            new_string = re.search("(?P<url>https?://[^\s]+)", mystring).group("url")
            return urlgrabber(mystring.replace(new_string, "x"), a_list)
    except AttributeError:
        return a_list


print(urlgrabber(myString))




