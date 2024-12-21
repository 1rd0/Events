from tortoise import models, fields

class Tournament(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    start_date = fields.DateField()
    end_date = fields.DateField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tournaments"

class Game(models.Model):
    id = fields.IntField(pk=True)
    tournament = fields.ForeignKeyField("models.Tournament", related_name="games")
    name = fields.CharField(max_length=255)
    scheduled_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "games"
