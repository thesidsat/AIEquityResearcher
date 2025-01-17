from typing import Dict, List, Tuple, Optional
import instructor
from openai import OpenAI
from pydantic import BaseModel

def generate_insights_for_sections(report: Dict, model: str):
    """Generate LLM insights for each section of the report."""
    class Insight(BaseModel):
        insight: str
        signal: int
    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        ),
        mode=instructor.Mode.JSON,
    )
    
    if "sections" not in report:
        raise ValueError("Report must contain a 'sections' key")
    
    for section in report["sections"]:
        content = section.get("data", "")
        section_name = section.get("name", "Unknown Section")
        
        prompt = f"""
        Analyze the provided {section_name} data in the context of a comprehensive Equity Research report. 
        Deliver clear and concise insights, including actionable recommendations, while highlighting key risks and opportunities. 
        Based on your analysis, assign a signal: Buy 1, Sell -1, or Hold 0
        {content}
        """
        
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_model=Insight,
            )
            section["insight"] = resp.insight
            section["signal"] = resp.signal
        except Exception as e:
            section["insight"] = f"Error generating insight: {e}"
            section["signal"] = 0
    
    return report
