from server import mcp
from dotenv import load_dotenv
import tools.get_resolution_issue

load_dotenv()

def main():
    mcp.run()

if __name__ == "__main__":
    main()
