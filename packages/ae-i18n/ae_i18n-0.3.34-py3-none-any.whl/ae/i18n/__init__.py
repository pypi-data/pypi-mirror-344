"""
internationalization / localization helpers
===========================================

on importing this portion, it will automatically determine the default locale (language) and encoding of your operating
system and user configuration.

the functions :func:`default_language` and :func:`default_encoding` - provided by this portion - are determining or
changing the default language and translation texts encoding.

additional languages will be automatically loaded by the function :func:`load_language_texts`.


translation texts files
-----------------------

translation files can be provided by your app as well as any python package and namespace portion to store translation
texts. by default, they are situated in a subfolder with the name `loc` underneath of your app/package root folder. to
load them, call the function :func:`register_package_translations` from the module using the locale texts.

translation files get loaded and merged automatically when the module is imported. the translation texts provided by
this portion will be loaded first. later imported packages would overwrite the translations with the same message id
of earlier imported packages.

e.g., the ae portion :mod:`ae.gui` is automatically loading and merging their package/module specific
translation messages on module/package import and could overwrite some of the translations provided by
this portion.

you can use the function :func:`register_translations_path` to specify additional locale folders with translation texts.

in a locale folder has to exist for each supported language a subfolder named as the language code
(e.g. 'loc/en' for English). and in each of these subfolders has to exist at least one message translation file
with a file name ending in the string specified by the constant :data:`MSG_FILE_SUFFIX`.

the content of these files has to be a valid python literal string that can be evaluated into a dictionary of
translation texts. the message to translate is the dictionary key, and the dict value is either a string with the
translated text or another dictionary of translations for a pluralized message.

the following example shows the content of a translation file with 3 translatable message ids, the first one
without pluralization, the second one with a single translation and the third one with all five possible
pluralized translation forms::

    {
        "simple translatable message": "translated message text",
        "simple pluralizable message": {'zero': "translated text if count == 0"},
        "{count} children": {
           'zero':      "no children",        # {count} would be replaced with `'0'`
           'one':       "one child",          # help text if count == 1
           'many':      "{count} children",
           'negative':  "missing children",
           '':          "undefined children"  # fallback help text if count is None
        },
    }

the `count` value can be specified as a keyword argument to the translation functions :func:`get_text`
and :func:`get_f_string`.


translation functions
---------------------

simple message text strings can be enclosed in the code of your application with the :func:`get_text` function provided
by this portion/module::

    from ae.i18n import get_text

    message = get_text("any translatable message displayed to the app user.")
    print(message) # prints the translated message text

for more complex messages with placeholders, you can use the :func:`get_f_string` function::

    from ae.i18n import get_f_string

    my_var = 69
    print(get_f_string("The value of my_var is {my_var}."))

.. note::
    to ensure the translation text can be found in the message file, do **not** declare the message argument
    passed to :func:`get_f_string` as an f-string expression (with an 'f' prefix).

translatable message can also be provided in various pluralization forms. to get a pluralized message, you have to pass
the :paramref:`~get_text.count` keyword argument of :func:`get_text`::

    print(get_text("child", count=1)) # translated into "child" (in English) or e.g. "Kind" in german
    print(get_text("child", count=3)) # -> "children" (in English) or e.g. "Kinder" (in german)

for pluralized message translated by the :func:`get_f_string` function, the count value has to be passed in the `count`
item of the :paramref:`~get_f_string.loc_vars`::

    print(get_f_string("you have {count} children", loc_vars=dict(count=1)))
    # -> "you have 1 child" or e.g. "Sie haben 1 Kind"
    print(get_f_string("you have {count} children", loc_vars={'count': 3}))
    # -> "you have 3 children" or "Sie haben 3 Kinder"

you can load several languages into your app run-time. to get the translation for a language that is not the current
default language, you have to pass the :paramref:`~get_text.language` keyword argument with the desired language code
onto the call of :func:`get_text` or :func:`get_f_string`::

    print(get_text("message", language='es')) # returns the Spanish translation text of "message"
    print(get_text("message", language='de')) # returns the German translation text of "message"

.. hint::
    the ae portion :mod:`ae.kivy.i18n` is implementing additional translation
    and helper functions, especially for kv files and the Kivy framework.

the helper function :func:`translation` can be used to determine if a translation exists for a message text.
"""
import ast
import locale
import os
from typing import Any, Dict, List, Optional, Union

from ae.base import norm_path, os_platform, stack_var, stack_vars                           # type: ignore
from ae.files import read_file_text                                                         # type: ignore
from ae.paths import Collector, normalize                                                   # type: ignore
from ae.dynamicod import try_eval                                                           # type: ignore


__version__ = '0.3.34'


MsgType = Union[str, Dict[str, str]]                        #: type of message literals in translation text files
LanguageMessages = Dict[str, MsgType]                       #: type of the data structure storing the loaded messages


DEF_ENCODING = 'UTF-8'                                      #: encoding of the messages in your app code
DEF_LANGUAGE = 'en'                                         #: language code of the messages in your app code

INSTALLED_LANGUAGES: List[str] = []                         # list of language codes found in :data:`TRANSLATIONS_PATHS`

LOADED_TRANSLATIONS: Dict[str, LanguageMessages] = {}       #: message text translations of all loaded languages

MSG_FILE_SUFFIX = 'Msg.txt'                                 #: name suffix of translation text files

TRANSLATIONS_PATHS: List[str] = []                          #: file paths to search for translations


if os_platform == 'android':                                                                        # pragma: no cover
    from jnius import autoclass                                                                     # type: ignore

    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
    # noinspection PyBroadException
    try:
        # copied from https://github.com/HelloZeroNet/ZeroNet-kivy/blob/master/src/platform_android.py
        _LANG = mActivity.getResources().getConfiguration().locale.toString()   # deprecated since API level 24
    except Exception:                                   # pylint: disable=broad-except
        # noinspection PyBroadException
        try:
            _LANG = mActivity.getResources().getConfiguration().getLocales().get(0).toString()
        except Exception:                               # pylint: disable=broad-except
            _LANG = ''
    _ENC = ''
else:
    _LANG, _ENC = locale.getdefaultlocale()  # type: ignore # mypy is not seeing the not _LANG checks (next code line)
if not _LANG:
    _LANG = DEF_LANGUAGE     # pragma: no cover
elif '_' in _LANG:
    _LANG = _LANG.split('_')[0]
if not _ENC:
    _ENC = DEF_ENCODING      # pragma: no cover
default_locale: List[str] = [_LANG, _ENC]               #: language and encoding code of the current language/locale
del _LANG, _ENC


def default_encoding(new_enc: str = '') -> str:
    """ get and optionally set the default message text encoding.

    :param new_enc:             new default encoding to be set. kept unchanged if not passed.
    :return:                    old default encoding (current if :paramref:`~default_encoding.new_enc` get not passed).
    """
    old_enc = default_locale[1]
    if new_enc:
        default_locale[1] = new_enc
    return old_enc


def default_language(new_lang: str = '') -> str:
    """ get and optionally set the default language code.

    :param new_lang:            new default language code to be set. kept unchanged if not passed.
    :return:                    the old default language (or the current one when :paramref:`~default_language.new_lang`
                                 gets not passed).
    """
    old_lang = default_locale[0]
    if new_lang:
        default_locale[0] = new_lang
        if new_lang not in LOADED_TRANSLATIONS:
            load_language_texts(new_lang)
    return old_lang


def get_text(text: str, count: Optional[int] = None, key_suffix: str = '', language: str = '') -> str:
    """ translate passed text string into the current language.

    :param text:                text message to be translated.
    :param count:               pass int value if the translated text has variants for their pluralization. the count
                                value will be converted into an amount/pluralize key by the function :func:`plural_key`.
    :param key_suffix:          suffix to the key used if the translation is a dict.
    :param language:            language code to load (def=current language code in 1st item of :data:`default_locale`).
    :return:                    translated text message or the value passed into :paramref:`~get_text.text` if no
                                translation text got found for the current language.
    """
    trans = translation(text, language=language)
    if isinstance(trans, str):
        text = trans
    elif trans is not None:
        text = trans.get(plural_key(count) + key_suffix, text)
    return text


def get_f_string(f_str: str, key_suffix: str = '', language: str = '',
                 glo_vars: Optional[Dict[str, Any]] = None, loc_vars: Optional[Dict[str, Any]] = None
                 ) -> str:
    """ translate the passed f-string into a message string of the passed / default language.

    :param f_str:               f-string to be translated and evaluated.
    :param key_suffix:          suffix to the key used if the translation is a dict.
    :param language:            language code to load (def=current language code in 1st item of :data:`default_locale`).
    :param glo_vars:            global variables used in the conversion of the f-string expression to a string. the
                                globals() of the caller of the callee will be available too and get overwritten by the
                                items of this argument.
    :param loc_vars:            local variables used in the conversion of the f-string expression to a string. the
                                locals() of the caller of the callee will be available too and get overwritten by the
                                items of this argument. pass a numeric value in the `count` item of this dict for
                                pluralized translated texts (see also :paramref:`~get_text.count` parameter of the
                                function :func:`get_text`).
    :return:                    translated text message including evaluated and formatted variables/expressions of the
                                f-string passed-in :paramref:`~get_f_string.f_str`. if no translation text got found for
                                the current language, then the original text message will be returned. any syntax errors
                                and exceptions occurring in the conversion of the f-string are silently ignored.
    """
    count = loc_vars.get('count') if isinstance(loc_vars, dict) else None
    f_str = get_text(f_str, count=count, key_suffix=key_suffix, language=language)

    ret = ''
    if '{' in f_str and '}' in f_str:  # performance optimization: skip f-string evaluation if no placeholders
        g_vars, l_vars, _ = stack_vars(max_depth=1)
        if glo_vars is not None:
            g_vars.update(glo_vars)
        if loc_vars is not None:
            l_vars.update(loc_vars)

        ret = try_eval('f"""' + f_str + '"""', ignored_exceptions=(Exception, ), glo_vars=g_vars, loc_vars=l_vars)

    return ret or f_str


def load_language_file(file_name: str, encoding: str, language: str):
    """ load file content encoded with the given encoding into the specified language.

    :param file_name:           file name, inclusive path and extension to load.
    :param encoding:            encoding id string.
    :param language:            language id string.
    """
    content = read_file_text(file_name, encoding=encoding)
    if content:
        lang_messages = ast.literal_eval(content)
        if lang_messages:
            if language not in LOADED_TRANSLATIONS:
                LOADED_TRANSLATIONS[language] = {}
            LOADED_TRANSLATIONS[language].update(lang_messages)


def load_language_texts(language: str = '', encoding: str = '', domain: str = '', reset: bool = False) -> str:
    """ load translation texts for the given language and optional domain.

    :param language:            language code of the translation texts to load. use the default language if not passed.
    :param encoding:            encoding to use to load the message file.
    :param domain:              optional domain id, e.g., the id of an app, attached process or a user. if specified,
                                then it will be used as the prefix for the message file name to be loaded additionally
                                and after the default translation texts get loaded (overwriting the default
                                translations).
    :param reset:               pass True to clear all previously added language/locale messages.
    :return:                    language code of the loaded/default language.
    """
    if not language:
        language = default_language()
    if not encoding:
        encoding = default_locale[1]
    if reset:
        LOADED_TRANSLATIONS.clear()

    for root_path in TRANSLATIONS_PATHS:
        file_path = os.path.join(root_path, language, MSG_FILE_SUFFIX)
        if os.path.exists(file_path):
            load_language_file(file_path, encoding, language)
        file_path = os.path.join(root_path, language, domain + MSG_FILE_SUFFIX)
        if os.path.exists(file_path):
            load_language_file(file_path, encoding, language)

    return language


def plural_key(count: Optional[int]) -> str:
    """ convert the number in :paramref:`~plural_key.count` into a dict key to access the correct plural form.

    :param count:               number of items used in the current context or None (resulting in empty string).
    :return:                    dict key (prefix) within the MsgType part of the translation data structure.
    """
    if count is None:
        key = ''
    elif count == 0:
        key = 'zero'
    elif count == 1:
        key = 'one'
    elif count > 1:
        key = 'many'
    else:
        key = 'negative'

    return key


def register_package_translations():
    """ call from the module scope of the package to register/add the translation resources path.

    no parameters are needed because we use the :func:`~ae.base.stack_var` helper function to determine the
    module file path via the `__file__` module variable of the caller module in the call stack. in this call
    we have to overwrite the default value (:data:`~ae.base.SKIPPED_MODULES`) of the
    :paramref:`~ae.base.stack_var.skip_modules` parameter to not skip ae portions that are providing
    translation message resources and are listed in the :data:`~ae.base.SKIPPED_MODULES`, like e.g.
    :mod:`ae.gui` (passing empty string '' to overwrite the default skip list).
    """
    package_path = os.path.dirname(norm_path(stack_var('__file__', '')))
    register_translations_path(package_path)


def register_translations_path(translation_path: str = "") -> bool:
    """ add/register the passed root path as a new resource of translation texts.

    :param translation_path:    root path of a translation folder structure to register, using cwd if not specified.
    :return:                    True if the translation folder structure exists and got properly added/registered,
                                else False.
    """
    translation_path = normalize(os.path.join(translation_path, 'loc'))
    if not os.path.exists(translation_path):
        return False

    coll = Collector()
    coll.collect(translation_path, select="**/*" + MSG_FILE_SUFFIX)
    for file_path in coll.files:
        if file_path.endswith(MSG_FILE_SUFFIX):
            lang_path = os.path.basename(os.path.dirname(file_path))
            if lang_path not in INSTALLED_LANGUAGES:
                INSTALLED_LANGUAGES.append(lang_path)

    if translation_path not in TRANSLATIONS_PATHS:
        TRANSLATIONS_PATHS.append(translation_path)

    return True


def translation(text: str, language: str = '') -> Optional[Union[str, MsgType]]:
    """ determine translation for passed text string and language.

    :param text:                text message to be translated.
    :param language:            language code to load (def=current language code in 1st item of :data:`default_locale`).
    :return:                    None, if not found, else the translation message string or dict with plural forms.
    """
    if not language:
        language = default_locale[0]

    if language in LOADED_TRANSLATIONS:
        translations = LOADED_TRANSLATIONS[language]
        if text in translations:
            return translations[text]
    return None


register_package_translations()
