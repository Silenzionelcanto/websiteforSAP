import  json
data='''
{
"name" : "A",
"phone": { "type" : "intl", "number" : "+1 23456" },
"email" : {"hide" : "yes"}
}'''
info = json.loads(data)
print(info["name"])