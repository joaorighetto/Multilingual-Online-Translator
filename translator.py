import requests
from bs4 import BeautifulSoup


supported_languages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                       8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}

print("Hello, welcome to the translator. Translator supports:")
for key, pair in supported_languages.items():
    print(f"{key}. {pair}")

language_from = int(input("Type the number of your language:"))
language_to = int(input("Type the number of language you want to translate to:"))
word_to_translate = input("Type the word you want to translate:")


url = f"https://context.reverso.net/translation/{supported_languages[language_from].casefold()}-{supported_languages[language_to].casefold()}/{word_to_translate}"

headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers=headers)

if page.status_code == 200:

    soup = BeautifulSoup(page.content, "html.parser")
    print(f"{supported_languages[language_to]} Translations:")
    words = []
    for word in soup.find_all(class_="display-term"):
        words.append(word.text)
    for word in words:
        print(word)

    print()

    print(f"{supported_languages[language_to]} Examples:")
    examples = []
    section = soup.find("section", {"id": "examples-content"})
    for div in section.find_all("div", {"class": "example"}):
        for span in div.find_all("span", {"class": "text"}):
            examples.append(span.text.strip())
    for i in range(0, len(examples), 2):
        print(examples[i])
        print(examples[i+1])
        print()
else:
    print(f"Error {page.status_code}, try again.")
