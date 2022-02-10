from orbe.utils import load_json, dump_json

dict_test = {
    "foo": "bar",
    "zoo": "var"
}

#dump_json("test.json", dict_test)

print(load_json("test.json"))

dict_test.update({"foo": "reeeeeeeee"})

dump_json("test.json", dict_test)

print(load_json("test.json"))