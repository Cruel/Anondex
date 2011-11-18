from django.db.models.signals import post_syncdb
from django.db import connection, transaction

from adex import models

# Set item_code field to be BINARY, to force case-sensitive comparisons
def set_name_to_binary(sender, **kwargs):
    print "Changing adex_adex to BINARY . . ."
    cursor = connection.cursor()
    cursor.execute('ALTER TABLE adex_adex MODIFY item_code VARCHAR(12) BINARY NOT NULL')
    transaction.commit_unless_managed()

post_syncdb.connect(set_name_to_binary, sender=models)