import requests
from bs4 import BeautifulSoup

target_language = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
word_to_translate = input('Type the word you want to translate:')

print(f'You chose "{target_language}" as a language to translate "{word_to_translate}".')


if target_language == "fr":
    url = f"https://context.reverso.net/translation/english-french/{word_to_translate}"
elif target_language == "en":
    url = f"https://context.reverso.net/translation/french-english/{word_to_translate}"
else:
    print("Please choose 'fr' or 'en'.")
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers=headers)
status = page.status_code
if status == 200:
    print(f"{status} OK")
    print("Translations")
    soup = BeautifulSoup(page.content, "html.parser")

    words = []
    for word in soup.find_all(class_="display-term"):
        words.append(word.text)
    print(words)

    phrases = []
    section = soup.find("section", {"id": "examples-content"})
    for div in section.find_all("div", {"class": "example"}):
        for span in div.find_all("span", {"class": "text"}):
            phrases.append(span.text.strip())
    print(phrases)

else:
    print(f"Error {page.status_code}, try again.")
