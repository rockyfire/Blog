from django.contrib.syndication.views import Feed

from .models import Post

class AllPostsRssFeed(Feed):

    title="Django blog project"

    link="/"

    description="Django project test"

    def items(self):
        return Post.objects.all()

    def items_title(self,item):
        return '[%s] %s' % (item.category,item.title)

    def item_description(self, item):
        return item.content
