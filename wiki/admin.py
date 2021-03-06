import wiki.models
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug" : ('title',) }


class RevisionAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(wiki.models.Article, ArticleAdmin)
admin.site.register(wiki.models.Revision, RevisionAdmin)