import urllib.parse
import urllib.request
import json
import re
import sys
from jinja2 import Environment, PackageLoader, select_autoescape

def italicize_sentence_label(sentence):
   return re.sub(r'(^|\. *)([^:\.]*:)', '\\1<i>\\2</i>', sentence)

def modifier_value_to_str(modifier_value):
   plus = ""
   if modifier_value >= 0:
      plus = "+"
   return "{plus}{value:1.0f}".format(plus=plus, value=modifier_value)

def attribute_modifier(attribute):
   modifier_value = (attribute / 2) - 5;
   return modifier_value_to_str(modifier_value)

def open5e_render_html(uri):
   url = "https://api.open5e.com/v1/{uri}".format(uri=uri)
   jinja_env = Environment(
       loader=PackageLoader("src.open5e"),
       autoescape=select_autoescape(),
       extensions=["jinja2.ext.do",]
   )
   jinja_env.globals.update(
      attribute_modifier=attribute_modifier,
      modifier_value_to_str=modifier_value_to_str,
      italicize_sentence_label=italicize_sentence_label,
      any=any,
   )
   classification, remainder = uri.split('/', 1)
   template = jinja_env.get_template("{classification}.tmpl".format(classification=classification))

   user_agent = 'bot-rpg/1.0'
   headers = {'User-Agent': user_agent}

   req = urllib.request.Request(url, None, headers)
   with urllib.request.urlopen(req) as response:
      data = response.read()
      dict = json.loads(data)
      return template.render(dict)

if __name__ == "__main__":
   args = sys.argv[1:]
   html = open5e_render_html(args[0])
   print(html)
