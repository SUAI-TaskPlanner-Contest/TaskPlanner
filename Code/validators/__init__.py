from datetime import datetime
from pydantic import StrictStr, StrictInt
from pydantic import BaseModel, validator
from email_validator import validate_email
from urllib.parse import urlparse

from .server import ServerValidate
from .task import TaskValidate
from .label import LabelValidate
from .category import CategoryValidator