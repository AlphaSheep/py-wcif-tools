import os


PORT: int = int(os.getenv("PY_WCIF_TOOLS_PORT", "4299"))

WCA_HOST: str = os.getenv("WCA_HOST", "http://localhost:3000")
WCA_API_KEY: str = os.getenv("WCA_API_KEY", "example-application-id")

