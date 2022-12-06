import requests
from bs4 import BeautifulSoup


def find_translations(soup_obj):
    translations_ = []
    for translation_ in soup_obj.find_all(class_="display-term"):
        translations_.append(translation_.text)
    return translations_


def find_examples(soup_obj):
    examples_ = []
    for div in soup_obj.find("section", {"id": "examples-content"}).find_all("div", {"class": "example"}):
        for span in div.find_all("span", {"class": "text"}):
            examples_.append(span.text.strip())
    return examples_


def make_soup(link):
    h = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(link, headers=h)
    try:
        s = BeautifulSoup(r.content, "html.parser")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return s


supported_languages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                       8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}

print("Hello, welcome to the translator. Translator supports:")
for key, pair in supported_languages.items():
    print(f"{key}. {pair}")

language_from = int(input("Type the number of your language:"))
language_to = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:"))
word_to_translate = input("Type the word you want to translate:")

if language_to == 0:
    with open(f"{word_to_translate}.txt", "w") as file:
        for target_language in supported_languages.values():
            if target_language != supported_languages[language_from]:

                url = f"https://context.reverso.net/translation/{supported_languages[language_from].casefold()}-" \
                      f"{target_language.casefold()}/{word_to_translate}"

                soup = make_soup(url)

                translations = find_translations(soup)
                examples = find_examples(soup)

                print(f"{target_language} Translations:\n{translations[0]}\n")
                print(f"{target_language} Examples:\n{examples[0]}\n{examples[1]}\n")

                file.write(f"{target_language} Translations:\n{translations[0]}\n\n")
                file.write(f"{target_language} Examples:\n{examples[0]}\n{examples[1]}\n\n")

else:
    url = f"https://context.reverso.net/translation/{supported_languages[language_from].casefold()}-" \
          f"{supported_languages[language_to].casefold()}/{word_to_translate}"
    soup = make_soup(url)
    with open(f"{word_to_translate}.txt", "w") as file:

        print(f"{supported_languages[language_to]} Translations:")
        translations = find_translations(soup)

        file.write(f"{supported_languages[language_to]} Translations:\n")
        file.write("\n".join(translations))
        file.write("\n\n")

        for translation in translations:
            print(translation)

        print()

        file.write(f"{supported_languages[language_to]} Examples:\n")

        print(f"{supported_languages[language_to]} Examples:")
        examples = find_examples(soup)
        for i in range(0, len(examples), 2):
            print(f"{examples[i]}\n{examples[i+1]}\n")
            file.write(examples[i])
            file.write("\n")
            file.write(examples[i+1])
            file.write("\n\n")






