from google.adk.agents import LlmAgent
from .tools import calculate_spending_by_tag

calculate_spendings = LlmAgent(
    name="calculate_spendings",
    model="gemini-2.5-pro",
    description="Calculates spending totals from stored transactions, overall or by tag.",
    instruction="""Use calculate_spending_by_tag to compute totals. Provide breakdowns by tag if requested, 
    or overall spendings. Assume transactions have 'amount' and 'tag' fields.""",
    tools=[calculate_spending_by_tag]
)