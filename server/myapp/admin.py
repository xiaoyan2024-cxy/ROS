from django.contrib import admin

# Register your models here.
from myapp.models import Classification, Algorithm, Thing, Tag, User, Comment

admin.site.register(Classification)
admin.site.register(Algorithm)
admin.site.register(Tag)
admin.site.register(Thing)
admin.site.register(User)
admin.site.register(Comment)
