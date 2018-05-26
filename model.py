from bson import json_util
from mongoengine import *
import datetime


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class News(Document):
    title = StringField()
    body = StringField()
    created_when = DateTimeField(default=datetime.datetime.now())
    tags = ListField(StringField())
    modified_when = DateTimeField()

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(self.id)
        if 'created_when' in data:
            data['created_when'] = self.created_when.timestamp()

        if 'modified_when' in data:
            data['modified_when'] = self.modified_when.timestamp()


        return json_util.dumps(data)
