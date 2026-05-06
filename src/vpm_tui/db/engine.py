"""Database engine setup."""

from sqlalchemy import create_engine

from vpm_tui.config import settings
from vpm_tui.utils.paths import ensure_dir

ensure_dir(settings.data_dir)

engine = create_engine(settings.database_url, echo=False)
