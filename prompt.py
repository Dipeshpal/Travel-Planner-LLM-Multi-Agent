prompt = """

Objective:
Generate a detailed, day-by-day itinerary tailored to the user's preferences, budget, and destination. If existing plans are provided, refine and enhance them by optimizing activities, accommodations, and logistics while preserving the user's intent. If no existing plans are provided, create a new itinerary from scratch. Include travel recommendations to enhance the experience (e.g., packing tips, local apps, or safety advice).

Requirements:

Itinerary Scope:
Include {'potential flights (outbound and return, with airline, flight number, times, and cost), ' if include_flights else ''}{'accommodation options (fitting budget, preferences, and location convenience), ' if include_hotels else ''}key attractions/activities (aligned with preferences, prioritizing unique experiences and avoiding overly crowded tourist spots), dining suggestions (reflecting preferences and local cuisine), and transportation options (e.g., public transit, rentals, walking).
Account for travel time between locations and realistic pacing (avoid overscheduling).
Incorporate local customs, cultural tips, or etiquette to enhance the traveler's experience.

Budget Management:
Ensure total costs (travel, accommodations, food, activities, etc.) stay within {budget}. Provide approximate cost breakdowns for each day.
Highlight cost-saving tips (e.g., free attractions, discount passes, or budget dining).

Enhancements to Existing Plans:
If existing plans are provided, identify gaps or inefficiencies (e.g., suboptimal timing, missing key attractions, or budget overruns) and suggest improvements.
Retain core elements of the user's plan unless they conflict with preferences, budget, or feasibility.

Travel Recommendations:
Include practical advice such as weather-appropriate clothing, local transportation apps, safety tips, or visa requirements.
Suggest backup activities for flexibility (e.g., indoor options for rainy days).

Output Format:
Provide the itinerary as a well-structured Markdown table with the following columns:
Day: Day number of the trip (e.g., Day 1).
Date: Specific date (e.g., May 2, 2025).
Time: Time range for each activity (e.g., 9:00 AM - 11:00 AM).
Activity: Description of the activity (e.g., Visit museum, Breakfast at café).
Location: Specific location or venue (e.g., Louvre Museum, Café XYZ).
Notes: Additional details (e.g., booking requirements, accessibility info).
Stay Type: Type of accommodation (e.g., Hotel, Airbnb, Hostel).
Hotel Name: Name of the recommended hotel or accommodation.
Hotel Rating: Star rating of the hotel (e.g., 4-star, 5-star).
Hotel Amenities: Key amenities offered (e.g., pool, spa, free breakfast).
Approx Cost Stay: Estimated cost for accommodation per night.
Restaurant: Recommended restaurant for meals.
Cuisine Type: Type of cuisine offered (e.g., Italian, Local, Fusion).
Restaurant Price Range: Price category (e.g., $, $$, $$$).
Food Approx Cost: Estimated cost for meals/snacks per day.
Fuel Cost: Estimated cost for transportation (e.g., fuel, transit fares).
Travel Time: Estimated time for transit between activities/locations.
{'Flight Details: Airline, flight number, departure/arrival times, and cost (if included). ' if include_flights else ''}
Weather Forecast: Expected weather conditions for the day (e.g., sunny, 75°F).
{'Hotel Booking Details: Booking platform, special offers, and contact information (if included). ' if include_hotels else ''}
Local Customs/Tips: Cultural norms, tipping etiquette, or practical advice (e.g., 'Tipping 10% is customary').
Ensure the table is clear, concise, and visually organized. Include a brief summary before the table outlining total estimated costs, key highlights, and any critical recommendations.

Edge Cases:
If the destination has limited information, use real-time search (if available) to gather current data on attractions, accommodations, or events.
If dates are invalid or unclear, assume a 7-day trip starting from the next feasible date and clarify assumptions in the response.
If budget is insufficient, prioritize free or low-cost activities and suggest ways to adjust (e.g., shorter stay, budget accommodations).
If preferences are vague, infer reasonable preferences based on destination (e.g., cultural sites for historic cities, outdoor activities for natural destinations).

Example Output Structure:
### Trip Itinerary: {destination} ({dates})
**Total Estimated Cost**: ${total_cost}  
**Highlights**: [Key attractions or unique experiences]  
**Recommendations**: [Packing tips, apps, or safety advice]  

| Day | Date | Time | Activity | Location | Notes | Stay Type | Hotel Name | Hotel Rating | Hotel Amenities | Approx Cost Stay | Restaurant | Cuisine Type | Restaurant Price Range | Food Approx Cost | Fuel Cost | Travel Time | {'Flight Details | ' if include_flights else ''}Weather Forecast | {'Hotel Booking Details | ' if include_hotels else ''}Local Customs/Tips |
|-----|------|------|----------|----------|-------|-----------|------------|-------------|-----------------|------------------|------------|-------------|------------------------|------------------|-----------|-------------|{'----------------| ' if include_flights else ''}-------------------|{'----------------------| ' if include_hotels else ''}--------------------|
| 1   | May 2, 2025 | 8:00 AM - 9:00 AM | Breakfast at local café | Café XYZ | Vegan options available | Hotel | Grand Palace Hotel | 5-star | Pool, Spa, Free WiFi | $100 | Sunrise Café | Local | $$ | $20 | $5 | 10 min | {'Flight AA123, 7:00 AM - 10:00 AM, $200 | ' if include_flights else ''}Sunny, 75°F | {'Book via Expedia, free cancellation until 24h before | ' if include_hotels else ''}Tipping 10% is customary |

Final Notes:
Ensure all activities are feasible within the given dates and budget.
Verify that recommendations align with the destination's seasonal events, weather, or cultural context.
If real-time data is unavailable, base the itinerary on reliable, up-to-date knowledge or clearly state assumptions.
"""