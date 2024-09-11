from celery import shared_task
from elasticsearch_dsl import connections
from .models import BlogPost
from .documents import BlogEntryDocument
from elasticsearch import Elasticsearch
# Create a connection to Elasticsearch (with SSL verification disabled for development)
es = Elasticsearch(
    ['https://172.31.208.1:9200'],
    http_auth=('elastic', 'oyP*_qQdhYQDvosmfOlT'),
    verify_certs=False
)

# Update the connection in Elasticsearch DSL
connections.add_connection('default', es)

@shared_task
def index_blog_post(blog_post_id):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
        # Initialize the index (create if not exists)
        BlogEntryDocument.init()
        # Create a document instance
        document = BlogEntryDocument(
            meta={'id': blog_post.id},
            title=blog_post.title,
            text=blog_post.content,
            created_at=blog_post.created_at
        )
        # Save the document to Elasticsearch
        document.save()
    except BlogPost.DoesNotExist:
        # Handle the case where the blog post does not exist
        print(f'BlogPost with id {blog_post_id} does not exist.')
