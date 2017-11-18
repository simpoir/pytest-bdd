"""Gherkin translations loader."""

import codecs
import json
import pkg_resources as pkg

from . import __name__ as PACKAGE_NAME
from . import types


# mapping with gherkin-language.json type name, bdd type and separator
LANG_TYPES_MAP = [
    ("feature", types.FEATURE, ": "),
    ("scenarioOutline", types.SCENARIO_OUTLINE, ": "),
    # EXAMPLES_VERTICAL seems specific to pytest_bdd
    ("examples", types.EXAMPLES, ":"),
    ("scenario", types.SCENARIO, ": "),
    ("background", types.BACKGROUND, ":"),
    ("given", types.GIVEN, ""),
    ("when", types.WHEN, ""),
    ("then", types.THEN, ""),
    ("and", None, ""),  # Unknown step type,
    ("but", None, ""),  # Unknown step type,
]
LANGS = {}


def get_language(lang_code):
    """Get feature parsing map for a different language.

    :param str lang_code: The language code.

    :return: a list of (prefix, step_type)
    """
    if not LANGS:
        load_translations(LANGS)
    try:
        return LANGS[lang_code]
    except KeyError:
        raise Exception(
            "no translation for language code '{}'".format(lang_code))


def load_translations(cache):
    """Load translations from gherkin-languages into the cache.

    :param dict cache: dict into which to load {lang_code: STEP_PREFIXES}
    """
    lang_file = pkg.resource_stream(PACKAGE_NAME, "gherkin-languages.json")
    utf8_reader = codecs.getreader("utf-8")
    translations = json.load(utf8_reader(lang_file))
    for lang_code, translation in translations.items():
        language = [
            ("@", types.TAG),
        ]
        for type_name, type_, separator in LANG_TYPES_MAP:
            try:
                prefixes = translation[type_name]
            except KeyError:  # pragma: no cover
                raise Exception(
                    "gherkin language definition for '{}' is incomplete."
                    " it does not have '{}'".format(lang_code, type_name))

            for prefix in prefixes:
                language.append((prefix + separator, type_))
        cache[lang_code] = language
