import re
import spacy
import phonenumbers
from email_validator import validate_email, EmailNotValidError

nlp = spacy.load("en_core_web_sm")

def parse_resume(text: str) -> dict:
    doc = nlp(text)

    emails = []
    phones = []
    names = []

    for token in doc.ents:
        if token.label_ == "PERSON":
            names.append(token.text)

    for word in text.split():
        try:
            email = validate_email(word).email
            emails.append(email)
        except EmailNotValidError:
            pass

    for match in phonenumbers.PhoneNumberMatcher(text, None):
        phones.append(phonenumbers.format_number(
            match.number, phonenumbers.PhoneNumberFormat.E164
        ))

    return {
        "candidate_name": names[0] if names else None,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "raw_text": text,
    }
