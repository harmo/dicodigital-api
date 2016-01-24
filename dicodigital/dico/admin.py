from django.contrib import admin
from . import models


class DefinitionDetailAdmin(admin.ModelAdmin):
	search_fields = ('word__label', 'text', )

class DefinitionAdmin(admin.StackedInline):
    model = models.Definition
    can_delete = True
    extra = 2


class WordAdmin(admin.ModelAdmin):
    inlines = (DefinitionAdmin, )


admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Definition, DefinitionDetailAdmin)