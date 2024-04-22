import time

from main import initiate_db

embedded_docs = [{'id': 'oihio',
                  'text': '“老朽恭喜万道友ndfgjdtyj了！',
                  'embedding': [-0.011518126353621483, 0.009573851712048054, 0.005499211605638266, 0.04461297392845154,
                                -0.020845189690589905, 0.021938877180218697, 0.0464412085711956, 0.03788768872618675,
                                0.03227674961090088, 0.047726526856422424, 0.07203223556280136, 0.036191586405038834,
                                0.03777901455760002, -0.04421761631965637, -0.038646966218948364, -0.05684249475598335,
                                -0.02382410131394863, -0.00042923196451738477]}
                 ]
chroma_collection = initiate_db()
start_indexing = time.time()
for doc in embedded_docs:
    chroma_collection.add(ids=[doc['id']], embeddings=[doc['embedding']], documents=[doc['text']])
    print([doc['embedding']], [doc['text']])
end_indexing = time.time()
print(f"索引时间：{(end_indexing - start_indexing) / 60 % 60:.4f}分({end_indexing - start_indexing:.4f}秒)")
