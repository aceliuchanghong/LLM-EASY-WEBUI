from main import initiate_db

chroma_collection = initiate_db()

id_to_query = 'oihio'  # replace with the ID you want to query
doc = chroma_collection.get(ids=id_to_query)
if doc:
    print(doc)
