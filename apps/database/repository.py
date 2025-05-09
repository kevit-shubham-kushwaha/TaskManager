from apps.database.base_repository import BaseRepository
from database import user_db, task_db


flask_user_repository = BaseRepository(
  collection=user_db
)

flask_task_repository = BaseRepository(
  collection=task_db
)


