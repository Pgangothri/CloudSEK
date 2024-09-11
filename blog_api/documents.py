from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from .models import BlogPost
PUBLISHER_INDEX = Index('elastic_demo')

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)




@PUBLISHER_INDEX.doc_type
class BlogEntryDocument(Document):
    
    user_id = fields.IntegerField(attr='id')
    fielddata=True
    title = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )
    text = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
                
            }
        },
    )
   

    class Django(object):
        model = BlogPost