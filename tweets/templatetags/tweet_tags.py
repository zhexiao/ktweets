from django import template
import re

# import register
register = template.Library()


@register.filter(name='convert_text_to_link')
def convert_text_to_link(text):
    pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
    pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

    text = pat1.sub(r'\1<a href="\2" target="_blank">\3</a>', text)
    text = pat2.sub(r'\1<a href="http:/\2" target="_blank">\3</a>', text)

    return text
