from medialibrary.models import LibraryFile
from django.contrib import admin

class LibraryFileAdmin(admin.ModelAdmin):
    actions=['really_delete_selected']
    list_display= ('__unicode__', 'thumbnail',)

    def get_actions(self, request):
        actions = super(LibraryFileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 adex library file was"
        else:
            message_bit = "%s adex library files were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

admin.site.register(LibraryFile, LibraryFileAdmin)