import os

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

schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=True,
)

schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)
schema.add_field(field_name="my_text", datatype=DataType.STRING)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="my_id"
)
index_params.add_index(
    field_name="my_vector",
    index_type="AUTOINDEX",
    metric_type="IP"
)
client.create_collection(
    collection_name="customized_setup",
    schema=schema,
    index_params=index_params
)
