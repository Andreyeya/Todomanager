from tortoise import fields, models


class Task(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    text = fields.TextField()
    is_completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tasks"