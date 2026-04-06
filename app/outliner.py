from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model = "llama-3.3-70b-versatile")

def outliner(state):
    research = state.get("research")
    topic = state.get("topic")
    prompt = f"""
    You are an expert Content Architect. Your goal is to transform raw research into a logical, high-converting article outline.

    ### SOURCE MATERIAL:
    {research}

    ### TASK:
    Create a detailed, hierarchical outline for a comprehensive article on {topic}.

    ### GUIDELINES:
    1. **Thematic Grouping**: Identify the 3-5 core pillars found in the research and turn them into H2 headings.
    2. **Logical Flow**: Arrange sections from foundational concepts to advanced insights/practical applications.
    3. **Evidence Mapping**: Under each subheading, include 2-3 bullet points summarizing the specific data, stats, or facts from the research to be used there.
    4. **Narrative Arc**: Include a compelling Introduction hook and a "Key Takeaways" Conclusion.

    ### OUTPUT FORMAT:
    - H1: [Title]
    - H2: [Section Name]
    - [Sub-point with specific research evidence]
    - [Sub-point]
    """
    response = llm.invoke(prompt)

    return {"outline": response.content}