from lesscode_options.options import define, options

define(name="ceshi", type_=str, default="hello world", help_="说明", callback=str)
define(name="age", type_=int, default=5, help_="年龄", callback=str)

print(options.ceshi)
print(type(options.age))

options.ceshi = "hello"
print(options.ceshi)
