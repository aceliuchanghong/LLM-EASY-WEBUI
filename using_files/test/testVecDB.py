import os
import random
# https://zhuanlan.zhihu.com/p/673500172
from pymilvus import MilvusClient, DataType

uri = 'https://in03-aa941e2a2cd2371.api.gcp-us-west1.zillizcloud.com'
token = os.getenv("MILVUS_API_TOKEN")

client = MilvusClient(
    uri=uri,
    token=token
)

# 简易使用,之后不采取
# client.create_collection(
#     collection_name="quick_setup",
#     dimension=5
# )

# schema = MilvusClient.create_schema(
#     auto_id=False,
#     enable_dynamic_field=True,
# )
#
# schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
# schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)
# schema.add_field(field_name="color", datatype=DataType.VARCHAR, max_length=200)
#
# index_params = client.prepare_index_params()
#
# index_params.add_index(
#     field_name="my_vector",
#     index_type="AUTOINDEX",
#     metric_type="IP"
# )
#
# client.create_collection(
#     collection_name="customized_setup",
#     schema=schema,
#     index_params=index_params
# )

# 4.1. Prepare data
data = [
    {"my_id": 0,
     "my_vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354,
                   0.9029438446296592],
     "color": "pink_8682"
     },
    {"my_id": 1,
     "my_vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104],
     "color": "red_7025"
     },
    {"my_id": 2,
     "my_vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185,
                   0.20785793220625592],
     "color": "orange_6781"
     },
    {"my_id": 3,
     "my_vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345],
     "color": "pink_9298"
     },
    {"my_id": 4,
     "my_vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184,
                   0.30337481143159106],
     "color": "red_4794"
     },
    {"my_id": 5,
     "my_vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383, -0.1446277761879955],
     "color": "yellow_4222"
     },
    {"my_id": 6,
     "my_vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192,
                   -0.8984947637863987],
     "color": "red_9392"
     },
    {"my_id": 7,
     "my_vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709,
                   0.5378064918413052],
     "color": "grey_8510"
     },
    {"my_id": 8,
     "my_vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872,
                   -0.6140360785406336],
     "color": "white_9381"
     },
    {"my_id": 9,
     "my_vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717,
                   -0.6980531615588608],
     "color": "purple_4976"
     }
]

data2 = [{"my_id": 52,
          "my_vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872,
                        -0.6140360785406336],
          "color": "white0_93801",
          "my_test": "02"
          }
         ]
# 4.2. Insert data
res = client.insert(
    collection_name="customized_setup",
    data=data2
)

print(res)

# 5.1. Prepare data

# colors = ["green", "blue", "yellow", "red", "black", "white", "purple", "pink", "orange", "brown", "grey"]
# data = [{
#     "id": i,
#     "vector": [random.uniform(-1, 1) for _ in range(5)],
#     "color": f"{random.choice(colors)}_{str(random.randint(1000, 9999))}"
# } for i in range(1000)]
#
# # 5.2. Insert data
# res = client.insert(
#     collection_name="customized_setup",
#     data=data[10:]
# )
#
# print(res)
#
# query_vectors = [
#     [0.041732933, 0.013779674, -0.027564144, -0.013061441, 0.009748648]
# ]
#
# # 6.2. Start search
# res = client.search(
#     collection_name="customized_setup",  # target collection
#     data=query_vectors,  # query vectors
#     limit=3,  # number of returned entities
# )
#
# print(res)
