import requests
from bs4 import BeautifulSoup
import argparse


def find_translations(soup_obj):
    translations_ = []
    for translation_ in soup_obj.find_all(class_="display-term"):
        translations_.append(translation_.text)
    if len(translations_) > 0:
        return translations_
    else:
        print(f"Sorry, unable to find {word_to_translate}")
        quit()


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
        print("Something wrong with your internet connection")
        raise SystemExit(e)
    return s


parser = argparse.ArgumentParser()
parser.add_argument("language_from")
parser.add_argument("language_to")
parser.add_argument("word_to_translate")

args = parser.parse_args()

supported_languages = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese",
                       "dutch", "polish", "portuguese", "romanian", "russian", "turkish", "all"]


language_from = args.language_from
language_to = args.language_to
word_to_translate = args.word_to_translate


if language_to not in supported_languages:
    print(f"Sorry, the program doesn't support {language_to}")
    quit()
elif language_from not in supported_languages:
    print(f"Sorry, the program doesn't support {language_from}")
    quit()
# try:
elif language_to == "all":  # translate to all languages available
    with open(f"{word_to_translate}.txt", "w") as file:
        for target_language in supported_languages:
            if target_language != language_from:

                url = f"https://context.reverso.net/translation/" \
                      f"{language_from}-{target_language}/" \
                      f"{word_to_translate}"

                soup = make_soup(url)

                translations = find_translations(soup)
                examples = find_examples(soup)
                target_language = target_language.capitalize()
                print(f"{target_language} Translations:\n{translations[0]}\n")
                print(f"{target_language} Examples:\n{examples[0]}\n{examples[1]}\n")

                file.write(f"{target_language} Translations:\n{translations[0]}\n\n")
                file.write(f"{target_language} Examples:\n{examples[0]}\n{examples[1]}\n\n")

else:  # translate to desired language
    url = f"https://context.reverso.net/translation/" \
          f"{language_from}-{language_to}/" \
          f"{word_to_translate}"

    soup = make_soup(url)
    translations = find_translations(soup)
    examples = find_examples(soup)

    print(f"{language_to} Translations:")
    for translation in translations:
        print(translation)

    print()

    print(f"{language_to} Examples:")
    for i in range(0, len(examples), 2):
        print(f"{examples[i]}\n{examples[i+1]}\n")

    with open(f"{word_to_translate}.txt", "w") as file:
        language_to = language_to.capitalize()

        file.write(f"{language_to} Translations:\n")
        file.write("\n".join(translations))
        file.write("\n\n")

        file.write(f"{language_to} Examples:\n")
        for i in range(0, len(examples), 2):
            file.write(examples[i])
            file.write("\n")
            file.write(examples[i+1])
            file.write("\n\n")







# except Exception as e:
#     print(type(e))
