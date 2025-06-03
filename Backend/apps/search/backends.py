from haystack.backends.elasticsearch7_backend import Elasticsearch7SearchBackend
from haystack.backends.elasticsearch7_backend import Elasticsearch7SearchEngine

class CustomElasticsearchBackend(Elasticsearch7SearchBackend):
    DEFAULT_ANALYZER = "standard"
    
    def __init__(self, connection_alias, **connection_options):
        super().__init__(connection_alias, **connection_options)
        
        # Custom settings
        self.settings = {
            'settings': {
                "analysis": {
                    "analyzer": {
                        "ngram_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "asciifolding", "haystack_ngram"]
                        },
                        "edgengram_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "asciifolding", "haystack_edgengram"]
                        }
                    },
                    "tokenizer": {
                        "haystack_ngram_tokenizer": {
                            "type": "nGram",
                            "min_gram": 3,
                            "max_gram": 15,
                        },
                        "haystack_edgengram_tokenizer": {
                            "type": "edgeNGram",
                            "min_gram": 2,
                            "max_gram": 15,
                            "side": "front"
                        }
                    },
                    "filter": {
                        "haystack_ngram": {
                            "type": "nGram",
                            "min_gram": 3,
                            "max_gram": 15
                        },
                        "haystack_edgengram": {
                            "type": "edgeNGram",
                            "min_gram": 2,
                            "max_gram": 15
                        }
                    }
                }
            }
        }

class CustomElasticsearchSearchEngine(Elasticsearch7SearchEngine):
    backend = CustomElasticsearchBackend