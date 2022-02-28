import fastapi as _fastapi

import service.services as _services
from controller import (review_pattern_controller, tag_controller,
                        task_controller, user_controller, task_time_controller)

_services.create_database()


app = _fastapi.FastAPI()

# app.config["SQLALCHEMY_ECHO"] = True


app.include_router(user_controller.router)
app.include_router(task_controller.router)
app.include_router(tag_controller.router)
app.include_router(review_pattern_controller.router)
app.include_router(task_time_controller.router)

