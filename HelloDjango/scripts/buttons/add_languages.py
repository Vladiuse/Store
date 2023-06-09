from buttons.models import Language

LANGS = [
    'html',
    'css',
    'js',
    'python',
    'php',
    'sql',
]


def delete_all_langs():
    Language.objects.all().delete()


def create_langs():
    for lang_name in LANGS:
        Language.objects.create(name=lang_name)
    print('Language created', Language.objects.count())


delete_all_langs()
create_langs()
