from server import mcp
from dotenv import load_dotenv
import tools.get_resolution_issue

load_dotenv()

if __name__ == "__main__":
    mcp.run()
