import base64
import zlib
def string_2_zip(data):
    stringified_object = data.encode("utf-8")
    compressed_file = zlib.compress(stringified_object)
    base64_string = base64.b64encode(compressed_file)
    return base64_string

def zip_2_string(data):
    base64_string = base64.b64decode(data)
    res = zlib.decompress(base64_string)
    res = res.decode()
    return res


if __name__ == "__main__":
    test_dict = {}
    test_dict[22]='a'
    print(test_dict)
    import json
    test_json = json.dumps(test_dict)
    print(test_json)
    print(json.loads(test_json))