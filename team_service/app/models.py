from tortoise import fields, models

class Team(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    captain_id = fields.IntField()  # ID капитана из User Service
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "teams"

class Registration(models.Model):
    id = fields.IntField(pk=True)
    team = fields.ForeignKeyField("models.Team", related_name="registrations")
    tournament_id = fields.IntField()  # ID турнира из Tournament Service
    status = fields.CharField(max_length=20, default="pending")  # pending/approved/rejected
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "registrations"
class TeamMember(models.Model):
    id = fields.IntField(pk=True)
    team = fields.ForeignKeyField("models.Team", related_name="members")  # Связь с командой
    user_id = fields.IntField()  # ID пользователя из User Service
    role = fields.CharField(max_length=100, default="player")  # Роль в команде (например, игрок или капитан)
    joined_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "team_members"
