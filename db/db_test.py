import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.llms.config import settings

print(settings.POSTGRES_URL)