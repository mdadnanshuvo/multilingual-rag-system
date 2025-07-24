from deep_translator import GoogleTranslator


def detect_language(text: str) -> str:
    """
    Detects whether the input text is in Bangla or English based on character analysis.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: 'bn' if the text is detected as Bangla, 'en' otherwise.
    """
    # Very basic language detection (you can improve it later)
    # Returns 'bn' for Bangla, 'en' for English
    bangla_chars = set("অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়")
    threshold = 0.3
    bangla_count = sum(1 for c in text if c in bangla_chars)
    ratio = bangla_count / max(len(text), 1)
    return "bn" if ratio > threshold else "en"


def translate_to_english(text: str) -> str:
    """
    Translates the given text to English using GoogleTranslator.

    Args:
        text (str): The input text to translate.

    Returns:
        str: The translated text in English.
    """
    return GoogleTranslator(source="auto", target="en").translate(text)


def translate_to_bangla(text: str) -> str:
    """
    Translates the given text to Bangla (Bengali).

    Args:
        text (str): The input text to be translated.

    Returns:
        str: The translated text in Bangla.
    """
    return GoogleTranslator(source="auto", target="bn").translate(text)
