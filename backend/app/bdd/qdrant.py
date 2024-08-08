import uuid

from qdrant_client import QdrantClient,models
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import CharacterTextSplitter

from app.models.models import embeddings

collection_name="PRUEBA41"

# client = QdrantClient(
#     host="localhost", port=6333
# )


# def create():
#     client.create_collection(
#     collection_name=collection_name,
#     sparse_vectors_config={
#         "text": models.SparseVectorParams(),
#     }
#     )
#create()

# doc_store = Qdrant(
#     client=client, collection_name=collection_name, 
#     embeddings=embeddings,
# )




query="Que es qdrant?"

texts=["""Qdrant es un motor de búsqueda y recuperación de vectores, diseñado para manejar datos de alta dimensión y permitir búsquedas eficientes basadas en similitudes. En Qdrant, los "points" (puntos) se refieren a los elementos o registros de datos que se almacenan en el motor de búsqueda. Cada "point" representa una entidad en el espacio vectorial y está compuesto por un identificador único (ID) y un vector de características.""",""" Conceptos Clave
Vector de Características: Es un arreglo de números que representa las características de un punto en un espacio de alta dimensión. Estos vectores son utilizados para calcular la similitud entre puntos.
ID del Punto: Un identificador único asignado a cada punto, que permite referenciarlo y acceder a él de manera eficiente.
Espacio Vectorial: Un espacio matemático donde cada punto tiene una ubicación definida por su vector de características.
Ejemplo de Uso
Supongamos que estás trabajando con un conjunto de datos de imágenes. Cada imagen puede ser representada por un vector de características extraído mediante una red neuronal. En Qdrant, cada imagen se almacenaría como un "point", donde el vector de características sería el vector de la imagen y el ID podría ser un identificador único de la imagen.

Operaciones Comunes
Inserción: Añadir nuevos puntos al motor de búsqueda.
Búsqueda por Similaridad: Encontrar puntos que son similares a un vector de consulta dado.
Actualización: Modificar el vector de características o el ID de un punto existente.
Eliminación: Remover puntos del motor de búsqueda.
Qdrant es especialmente útil en aplicaciones que requieren búsquedas rápidas y precisas basadas en similitud, como sistemas de recomendación, recuperación de información, y más."""]

qdrant = Qdrant.from_texts(
    texts,
    embeddings,
    url="http://localhost:6333",
    prefer_grpc=False,
    collection_name=collection_name,
)

print(qdrant.similarity_search(query))




# def create(create=True):
#     if create:
#         client.create_collection(
#             collection_name="test",
#             vectors_config=VectorParams(size=4098, distance=Distance.COSINE),
#         )
#         print(client.get_collection(collection_name="test2"))
#         return client

# client=create(create=True)

# def get_text_chunks(text):
#   text_splitter = CharacterTextSplitter(
#     separator="\n",chunk_size=5,chunk_overlap=0,length_function=len)
#   chunks = text_splitter.split_text(text)
#   return chunks

# def get_embedding(text_chunks):
#     points = []
#     for idx, chunk in enumerate(text_chunks):
#         response=embeddings.embed_query(text_chunks[idx])
#         vectors = response
#         point_id = str(uuid.uuid4())  # Generate a unique ID for the point
#         points.append(PointStruct(id=point_id, vector=vectors, payload={"text": chunk}))

#     return points

# def insert_data(get_points,client:QdrantClient):
#     client2 = QdrantClient(
#     host="localhost", port=6333
#     )
#     operation_info = client2.upsert(
#     collection_name="test2",
#     wait=True,
#     points=get_points
#     )
    
    
# chunks=get_text_chunks("""Qdrant es un motor de búsqueda y recuperación de vectores, diseñado para manejar datos de alta dimensión y permitir búsquedas eficientes basadas en similitudes. En Qdrant, los "points" (puntos) se refieren a los elementos o registros de datos que se almacenan en el motor de búsqueda. Cada "point" representa una entidad en el espacio vectorial y está compuesto por un identificador único (ID) y un vector de características.""")
# vectors=get_embedding(chunks)

# insert_data(vectors,client)

# def search(query):
#     query=embeddings.embed_query("Que es qdrant?")
#     return client.search(
#     collection_name="test2",
#     query_vector=query
#     )
    
# print(search(query))



    
# client.recreate_collection(
#    collection_name="my_collection",
#    vectors_config=VectorParams(size=769, distance=Distance.COSINE),
# )


# client.upsert(
#       collection_name="my_collection",
#       points=[
#             PointStruct(
#                id=i,
#                vector=
#             )
#             for i in range(100)
#       ],
#    )



# client.create_collection("test-collection-5", vectors_config=
#     VectorParams(
#         size=768,
#         distance=Distance.COSINE,
#     )
# )


# # The qdrant client from langchain
# store = Qdrant(
#     client=client, collection_name="test-collection-5", 
#     embeddings=embeddings,
# )

# points = [
#     PointStruct(
#         id=idx,
#         vector=response['embedding'],
#         payload={"text": text},
#     )
#     for idx, (response, text) in enumerate(zip(results, texts))
# ]

# client.upsert("test-collection-5", points)

# texts = [
#     "Qdrant is a vector database that is compatible with Gemini.",
#     "Gemini is a new family of Google PaLM models, released in December 2023.",
# ]

# store.aadd_texts(texts=texts)


# print(store.search("what is qdrant",search_type="mmr"))

