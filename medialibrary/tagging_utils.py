from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag

def get_tag_counts(model):
    table = model._meta.db_table
    content_type = ContentType.objects.get_for_model(model)
    tags = Tag.objects.raw('''SELECT t.id, t.name, COUNT(*) as count
          FROM tagging_tag AS t
                  INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
                  INNER JOIN `%s` ON tt.object_id = `%s`.`id`
          WHERE t.id IN (

            SELECT t.id FROM tagging_tag AS t
        INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
          WHERE tt.content_type_id = %d AND tt.object_id = %d

                  )
          GROUP BY t.id
          ORDER BY count DESC''' % (table, table, content_type.pk, model.pk))
    return tags