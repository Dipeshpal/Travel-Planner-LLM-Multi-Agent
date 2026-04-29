import os
from praisonaiagents import Agent, Agents, MCP


def _setup_llm_environment():
    """Setup environment variables for the selected LLM provider.

    Supports: groq, gemini, openrouter, openai
    Format: provider/model or openrouter/provider/model
    """
    llm_model = os.getenv("LLM_MODEL", "groq/deepseek-r1-distill-llama-70b")

    if llm_model.startswith("openrouter/"):
        openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        if openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
    elif llm_model.startswith("groq/"):
        groq_key = os.getenv("GROQ_API_KEY", "")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
    elif llm_model.startswith("gemini/"):
        google_key = os.getenv("GOOGLE_API_KEY", "")
        if google_key:
            os.environ["GOOGLE_API_KEY"] = google_key
    elif llm_model.startswith("openai/"):
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key

    return llm_model


def create_agents(api_key, search_provider, include_flight_agent=True, include_hotel_agent=True):
    """Create AI agents for travel planning with specified search provider.

    Args:
        api_key: API key for the search provider
        search_provider: "brave" or "firecrawl"
        include_flight_agent: Whether to include flight search agent
        include_hotel_agent: Whether to include hotel recommendation agent

    Returns:
        Agents instance with configured agents
    """
    if search_provider == "brave":
        mcp_tool = MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": api_key})
    else:
        mcp_tool = MCP("npx -y firecrawl-mcp", env={"FIRECRAWL_API_KEY": api_key})

    llm_model = _setup_llm_environment()
    agents_list = []

    research_agent = Agent(
        instructions="Research travel destinations, attractions, local customs, travel requirements, and seasonal events. Gather detailed information about unique experiences, cultural significance, weather patterns, local transportation options, safety considerations, and visa requirements. Identify off-the-beaten-path attractions that align with user preferences while avoiding overcrowded tourist spots. Research local etiquette, tipping customs, and cultural sensitivities to enhance the traveler's experience.",
        llm=llm_model,
        tools=mcp_tool
    )
    agents_list.append(research_agent)

    if include_flight_agent:
        flight_agent = Agent(
            instructions="Search for available flights, compare prices, and recommend optimal flight choices within the specified budget. Provide detailed information including airlines, flight numbers, departure/arrival times, layovers, baggage allowances, and total costs. Prioritize flights with the best balance of price, convenience, and comfort. Suggest alternative dates or nearby airports if they offer significant cost savings. Include booking platform recommendations and highlight any special offers or loyalty programs.",
            llm=llm_model,
            tools=mcp_tool
        )
        agents_list.append(flight_agent)

    if include_hotel_agent:
        hotel_agent = Agent(
            instructions="Research hotels and accommodation options that precisely match the user's budget and stated preferences. Provide comprehensive details including hotel name, star rating, location convenience, room types, amenities (pool, spa, free breakfast, etc.), and approximate costs per night. Consider proximity to planned activities and transportation options. Include booking details, cancellation policies, and special offers. For luxury preferences, focus on high-end amenities and exceptional service; for budget constraints, prioritize value and essential comforts.",
            llm=llm_model,
            tools=mcp_tool
        )
        agents_list.append(hotel_agent)

    planning_agent = Agent(
        instructions="Design detailed day-by-day travel plans incorporating activities, transportation, dining, and adequate rest time. Create balanced itineraries with realistic timing that account for travel between locations. Avoid overscheduling and allow flexibility. For each day, include specific time blocks for activities, estimated travel times between locations, recommended restaurants with cuisine types and price ranges, and approximate costs for all components. Ensure the total daily and trip costs stay within budget. Suggest backup activities for weather contingencies and include local transportation recommendations. If existing plans are provided, identify inefficiencies and suggest improvements while preserving core elements.",
        llm=llm_model,
        tools=mcp_tool
    )
    agents_list.append(planning_agent)

    return Agents(agents=agents_list)
