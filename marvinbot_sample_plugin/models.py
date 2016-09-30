import mongoengine
from marvinbot.utils import localized_date


# Plugin specific model, so as not to pollute the real users table
class WitnessedUser(mongoengine.Document):
    id = mongoengine.LongField(primary_key=True)
    first_name = mongoengine.StringField()
    last_name = mongoengine.StringField()
    username = mongoengine.StringField()

    date_added = mongoengine.DateTimeField(default=localized_date)

    @classmethod
    def by_id(cls, user_id):
        try:
            return cls.objects.get(id=user_id)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return "{id}: {username}".format(id=self.id, username=self.username or '<NoUserName>')
