from cleantext import clean

with open("input.txt", "r") as file:
    text: str = file.read()

cleaned_text: str = clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=False,
    normalize_whitespace=False,
    strip_lines=False,
    no_urls=True,
    no_emails=True,
    no_phone_numbers=True,
    no_currency_symbols=True
)

with open("output.txt", "w") as file:
    file.write(cleaned_text)
