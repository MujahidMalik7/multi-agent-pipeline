from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

def writer(state):
    research = state.get("research")
    outline = state.get("outline")
    decision = state.get("decision")
    revision_count = state.get("revision_count") 
    reason = state.get("reason")

    prompt = f"""
You are a Senior Technical Copywriter. Your mission is to transform the provided Outline and Research into a polished, publication-ready article.

### REFERENCE MATERIAL:
- **DETAILED OUTLINE**: 
{outline}

- **RAW RESEARCH DATA**: 
{research}

### WRITING DIRECTIVES:
1. **Stick to the Facts**: Use the specific statistics, names, and data points from the Research. Do not invent "placeholder" facts.
2. **Follow the Architecture**: Adhere strictly to the H1, H2, and H3 structure provided in the Outline.
3. **Voice & Tone**: Write in a professional yet conversational tone (authoritative, clear, and fluff-free). Avoid overused AI tropes like "In the rapidly evolving landscape... and try to make it as humanoid as possible..."
4. **Formatting**: Use Markdown for headers, bolding for emphasis, and bulleted lists to make the content scannable.
5. **Flow**: Ensure smooth transitions between sections so the article reads as one cohesive narrative, not a collection of notes.

### FINAL OUTPUT:
RETURN A DETAILED DRAFT
"""

    if decision == "rejected":
        revision_count +=1
        prompt += f"""
            ### **REVISION REASON**: {reason}
        """
        decision = None

    response = llm.invoke(prompt)

    return {
        "draft": response.content,
        "decision": decision,
        "revision_count": revision_count
        }