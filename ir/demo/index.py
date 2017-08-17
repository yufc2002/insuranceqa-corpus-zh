from config import *
from utils import bulk_index, warning_with_time


def read_type_from_ttl(file_path="tags.txt"):
    docs = {}
    with open(file_path, "r") as f:
        for line in f:
            iid = line.split()[0]
            tags = " ".join(line.strip().split()[1:])
            docs[iid] = {"tags": tags}
    return docs


if __name__ == "__main__":
    docs = read_type_from_ttl(file_path="tags.txt")
    print(warning_with_time("docs loaded"))

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "similarity": {
                "LM": { 
                "type": "LMJelinekMercer",
                "lambda":    0.4 
                }
            }
        },
        "mappings": {
            "text": {
                "properties": {
                    "tags": {
                        "type": "text",
                        "term_vector": "with_positions_offsets_payloads",
                        "store": True,
                        "analyzer": "standard",
                        "similarity": "LM"
                    }

                }
            }
        }
    }

    print(docs)
    ES.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    print("creating '%s' index..." % (INDEX_NAME))    
    res = ES.indices.create(index=INDEX_NAME, body=request_body)

    count = 1
    bulk_index(docs, 1, count)