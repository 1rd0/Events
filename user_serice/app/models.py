# app/models.py

from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    full_name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    teams: fields.ReverseRelation["Team"]
    registrations: fields.ReverseRelation["Registration"]

    class Meta:
        table = "users"

class Team(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    captain = fields.ForeignKeyField("models.User", related_name="teams", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    registrations: fields.ReverseRelation["Registration"]

    class Meta:
        table = "teams"

class Registration(models.Model):
    id = fields.IntField(pk=True)
    team = fields.ForeignKeyField("models.Team", related_name="registrations")
    tournament_id = fields.IntField()
    status = fields.CharField(max_length=20, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "registrations"
