import re

pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

# pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)


urlstr = 'http://www.example.com/foo/bar.html and this is a link https://zhexiao.com'

urlstr = pat1.sub(r'\1<a href="\2" target="_blank">\3</a>', urlstr)
# urlstr = pat2.sub(r'\1<a href="http:/\2" target="_blank">\3</a>', urlstr)

print(urlstr)