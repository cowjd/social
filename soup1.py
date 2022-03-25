from bs4 import BeautifulSoup
htmlString = '''<html>
<head><title>My Document</title></head>
<body>Main text.</body></html
'''

soup = BeautifulSoup(htmlString, "html.parser")
text = soup.get_text()
print(text)