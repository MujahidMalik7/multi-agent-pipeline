from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

tavily_search = TavilySearch(max_results = 3) ##Good for better results

def researcher(state):
    topic = state.get("topic")
    response = tavily_search.invoke(topic)
    
    #Extract the list (handle dict vs list return)
    result_list = response.get("results", []) if isinstance(response, dict) else []
    
    #Clean and join into a single string
    clean_response = "\n\n".join(
        [res.get("content", "") for res in result_list]
    )
    return {"research": clean_response}
