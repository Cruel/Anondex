import string
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from tagging.models import TagManager, Tag, TaggedItem
import tagging
from adex.models import Adex
from medialibrary.models import LibraryFile

class MyTagManager(TagManager):
    items = generic.GenericRelation(TaggedItem)
    def update_tags(self, obj, tag_names):
        tags = tag_names.split(',')
        for i, j in enumerate(tags):
            tags[i] = slugify(j)
        tag_names = ','.join(tags)
        return super(MyTagManager, self).update_tags(obj, tag_names)
    def add_tag(self, obj, tag_name):
        tag_name = slugify(tag_name)
        return super(MyTagManager, self).add_tag(obj, tag_name)
    def get_tag_counts(self, model):
        table = model._meta.db_table
        content_type = ContentType.objects.get_for_model(model)
        tags = self.raw(
            '''SELECT t.id, t.name, COUNT(*) as count
            FROM tagging_tag AS t
                INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
                INNER JOIN `%s` ON tt.object_id = `%s`.`id`
            WHERE t.id IN (
                SELECT t.id FROM tagging_tag AS t
                INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
                WHERE tt.content_type_id = %d AND tt.object_id = %d
            )
            GROUP BY t.id
            ORDER BY count DESC'''
                % (table, table, content_type.pk, model.pk)
        )
        return tags
    def get_tags_from_media(self, media_list):
        tags = set()
        for media_id in media_list:
            file = LibraryFile.objects.get(pk=media_id)
            tags = tags | set(self.get_for_object(file).values_list('name', flat=True))
        return list(tags)
    def get_related(self, tags):
        #TODO: merging the query sets does not increment the count properly ???
        tag_list1 = self.related_for_model(tags, LibraryFile, counts=True, min_count=None)
        tag_list2 = self.related_for_model(tags, Adex, counts=True, min_count=None)
        related_tags = list(set(tag_list1 + tag_list2))                 # Cast to set to remove duplicates
        related_tags.sort(key=lambda tag: tag.count, reverse=True)      # Sort tags with highest counts first
        return related_tags

class MyTag(Tag):
    objects = MyTagManager()
    class Meta:
        proxy = True

tagging.models.Tag = MyTag
tagging.fields.Tag = MyTag
