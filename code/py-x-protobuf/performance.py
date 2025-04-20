import book_pb2
import json
import timeit


def serialize_to_json(book):
    return json.dumps(book)

def serialize_to_protobuf(book):
    book = book_pb2.Book(isbn=book["isbn"], title=book["title"], author=book["author"], pagecount=book["pagecount"])
    return book.SerializeToString()

def deserialize_from_json(book: str):
    return json.loads(book)

def deserialize_from_protobuf(book: str):
    book_obj = book_pb2.Book()
    book_obj.ParseFromString(book)
    return book_obj


if __name__ == "__main__":

    book = dict(
        isbn="9781857232097",
        title="The Fires of Heaven",
        author="Robert Jordan",
        pagecount=912
    )
    trial_json = timeit.timeit("serialize_to_json(book)", number=10**6, globals=dict(serialize_to_json=serialize_to_json, book=book))

    trial_protobuf = timeit.timeit("serialize_to_protobuf(book)", number=10**6, globals=dict(serialize_to_protobuf=serialize_to_protobuf, book=book))

    print("Runtime results for serialization across 10^6 runs:")
    print(f"JSON={round(trial_json,4)}")
    print(f"protobuf={round(trial_protobuf,4)}")
    percentage_difference = round((trial_json-trial_protobuf)/trial_json*100,4)
    print(f"% difference={percentage_difference}")

    book_json = serialize_to_json(book)
    trial_json = timeit.timeit("deserialize_from_json(book_json)", number=10**6, globals=dict(deserialize_from_json=deserialize_from_json, book_json=book_json))
    book_protobuf = serialize_to_protobuf(book)
    trial_protobuf = timeit.timeit("deserialize_from_protobuf(book_protobuf)", number=10**6, globals=dict(deserialize_from_protobuf=deserialize_from_protobuf,book_protobuf=book_protobuf))
    percentage_difference = round((trial_json-trial_protobuf)/trial_json*100,4)
    print("Runtime results for deserialization across 10^6 runs:")
    print(f"JSON={round(trial_json,4)}")
    print(f"protobuf={round(trial_protobuf,4)}")
    print(f"% difference={percentage_difference}")
    

