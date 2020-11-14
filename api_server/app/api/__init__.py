from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import DbInfoApi
from app.api import OrganizationApi, FacultyApi, GroupApi
from app.api import ScheduleApi, ExamsApi
