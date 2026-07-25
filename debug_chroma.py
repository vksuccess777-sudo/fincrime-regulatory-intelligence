import chromadb

print("Chroma version:", chromadb.__version__)

client = chromadb.PersistentClient(path="tests/temp_chroma_db")
collection = client.get_or_create_collection("debug")

try:
    collection.delete(where={})
except Exception:
    pass

collection.add(
    ids=["1"],
    embeddings=[[1.0, 0.0]],
    metadatas=[{"test": "yes"}],
)

result = collection.query(
    query_embeddings=[[1.0, 0.0]],
    n_results=1,
    include=["embeddings", "metadatas", "distances"],
)

print("\nReturned keys:")
print(result.keys())

print("\nFull result:")
print(result)