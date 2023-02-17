from django.contrib import admin
from applications.post.models import Post, PostImage,Comment
from applications.feedback.models import Rating

from django.db.models import Avg 



class ImageAdmin(admin.TabularInline):
    model = PostImage
    fields = ('image',)
    max_num = 4

class PostAdmin(admin.ModelAdmin):
    inlines = (ImageAdmin,)
    list_display = ('title','owner','post_count','rating_count','created_at','john',)
    list_filter = ('owner',)
    search_fields = ('title',)
    # exclude = ('title', )
    exclude = ('john',)
        
    def post_count(self, obj):
        return obj.likes.filter(is_like = True).count()

    def rating_count(self, obj):
        return obj.ratings.aggregate(Avg('rating'))['rating__avg']





admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
admin.site.register(Comment)