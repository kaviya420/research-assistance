from ai_engine.rag.ollama_client import get_llm

def summarize_paper(text: str) -> dict:
    llm = get_llm()
    prompt = f"""
    You are an expert academic research assistant. 
    Analyze the following research paper text and extract the key information.
    Format your response exactly with these markers, do not omit them:
    
    [ABSTRACT]
    (write a short summary of what the paper is about)
    
    [METHODOLOGY]
    (describe the methods used)
    
    [RESULTS]
    (describe the key findings and results)
    
    [CONCLUSIONS]
    (describe the conclusions drawn by the authors)
    
    Text:
    {text[:8000]}
    """
    
    response = llm.invoke(prompt)
    
    summary = {
        "abstract": _extract_section(response, "[ABSTRACT]", "[METHODOLOGY]"),
        "methodology": _extract_section(response, "[METHODOLOGY]", "[RESULTS]"),
        "results": _extract_section(response, "[RESULTS]", "[CONCLUSIONS]"),
        "conclusions": _extract_section(response, "[CONCLUSIONS]", "")
    }
    return summary

def analyze_papers(papers_summaries: list) -> dict:
    if not papers_summaries or len(papers_summaries) < 2:
        return {"contradictions": "Need at least 2 papers for comparison.", "research_gaps": "Need more papers to identify gaps."}
        
    llm = get_llm()
    combined_text = ""
    for i, p in enumerate(papers_summaries):
        combined_text += f"\n--- Paper {i+1} ---\nAbstract: {p.get('abstract', '')}\nResults: {p.get('results', '')}\n"
        
    prompt = f"""
    You are an expert academic research assistant analyzing multiple research papers.
    Based on the summaries of multiple papers below, perform two tasks:
    1. Identify any CONTRADICTIONS between the findings of these papers (e.g., conflicting results or claims).
    2. Suggest potential RESEARCH GAPS (unexplored areas or areas needing further study).
    
    Format your response EXACTLY with these markers:
    
    [CONTRADICTIONS]
    (List any contradictions, or state "No major contradictions found" if none exist)
    
    [RESEARCH_GAPS]
    (List 2-3 potential research gaps)
    
    Papers context:
    {combined_text[:12000]}
    """
    
    response = llm.invoke(prompt)
    
    return {
        "contradictions": _extract_section(response, "[CONTRADICTIONS]", "[RESEARCH_GAPS]"),
        "research_gaps": _extract_section(response, "[RESEARCH_GAPS]", "")
    }

def _extract_section(text: str, start_marker: str, end_marker: str) -> str:
    try:
        start_idx = text.find(start_marker)
        if start_idx == -1: return ""
        start_idx += len(start_marker)
        
        if end_marker:
            end_idx = text.find(end_marker, start_idx)
            if end_idx == -1: end_idx = len(text)
        else:
            end_idx = len(text)
            
        return text[start_idx:end_idx].strip()
    except Exception:
        return ""
