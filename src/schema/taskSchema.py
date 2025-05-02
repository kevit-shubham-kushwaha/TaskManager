from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
  
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True, validate=validate.Length(min=3, max=100))
  description = fields.Str(required=True, validate=validate.Length(min=3, max=500))
  status = fields.Str(required=True, validate=validate.OneOf(['pending', 'in_progress', 'completed']))
  due_date = fields.Date(required=True)
  priority = fields.Str(required=True, validate=validate.OneOf(['low', 'medium', 'high']))
  assigned_to = fields.Str(required=True, validate=validate.Length(min=3, max=50))
  

