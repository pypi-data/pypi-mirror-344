from server import mcp
from utils.llm_call import make_llm_request

@mcp.tool()
async def get_issue_resolution(query:str) -> str:
    """
        Processes a user query describing an issue and returns a recommended resolution.

        This function takes in a natural language query from a user, representing a problem, 
        error, or issue they are facing. It forwards this query to an external language model 
        or AI service (such as an LLM API) that interprets the issue, analyzes the context, 
        and generates a suitable resolution or troubleshooting advice tailored to the query.

    Args:
        query (str): A natural language string containing the description of the 
        issue or problem for which a resolution is sought.

    Returns:
        str: A natural language string containing the recommended resolution, fix, or 
        next steps suggested by the AI for addressing the user's issue.
    """
    return await make_llm_request(query)