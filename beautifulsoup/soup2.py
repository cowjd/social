from bs4 import BeautifulSoup
from urllib.request import urlopen

htmlString = '''<html>
<head><title>My Document</title></head>
<body>Main text.</body></html>
'''

#soup = BeautifulSoup(htmlString, "html.parser")
soup = BeautifulSoup(urlopen("http://www.networksciencelab.com/"), "html.parser")

text = soup.get_text()
print(text)
print(soup)
soup