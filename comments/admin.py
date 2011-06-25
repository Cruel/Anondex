from comments.models import Comment, Image, User
from django.contrib import admin

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('question', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(User)
#admin.site.register(Comment, CommentAdmin)