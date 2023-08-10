from django.db import models

from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer,\
    JavascriptLexer, CssLexer, PhpLexer,SqlLexer, HtmlPhpLexer
from pygments.formatters import HtmlFormatter



LEXERS = {
    'html': HtmlLexer,
    'css': CssLexer,
    'js': JavascriptLexer,
    'python': PythonLexer,
    'php': PhpLexer,
    'sql': SqlLexer,
}
COLORED_STYLE = 'gruvbox-dark'

class Language(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class AbstractButton(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    text = models.TextField()
    type = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    colored_text = models.TextField(blank=True, editable=True)

    def save(self, **kwargs):
        if self.type:
            self.colored_text = self.get_colored_text()
        else:
            self.colored_text = ''
        super().save(**kwargs)

    def get_colored_text(self):
        lexer = LEXERS[self.type.name]
        code = highlight(self.text, lexer(encodings='utf-8'), HtmlFormatter())
        return code

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Button(AbstractButton):
    pass


class SubButton(AbstractButton):
    parent = models.ForeignKey(
        Button,
        on_delete=models.CASCADE,
        related_name='sub_button',
    )


class X(models.Model):
    name = models.CharField(max_length=30)
    x = models.CharField(max_length=30)
    y = models.CharField(max_length=30)

    def __str__(self):
        return self.name
