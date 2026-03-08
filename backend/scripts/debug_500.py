import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

try:
    from app.services.executive_service import fetch_executive_dashboard
    print("Calling fetch_executive_dashboard...")
    fetch_executive_dashboard("This Month", None, "All Channels", "All Regions", "All Segments")
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
