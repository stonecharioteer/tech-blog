import book_pb2

book = book_pb2.Book(isbn="9781857232097", title="The Fires of Heaven", author="Robert Jordan", pagecount=912)

serialized_book = book.SerializeToString()
# You can write this to a file if you want.

#You can deserialize this into a Book object if required.

book = book_pb2.Book()
book.ParseFromString(serialized_book)

print(f"{book.title} by {book.author}")
