
def validate_inputs(data):

    if not data["destination"]:
        return False,"Destination required",{}

    return True,"OK",data


def build_prompt(data):

    return f"""
Create a student travel itinerary.

Destination: {data['destination']}
Duration: {data['duration_days']} days
Budget: {data['budget_level']}
Transport: {data['transport']}
Stay: {data['stay_type']}
Interests: {data['interests']}

Return JSON format like:

{{
"daily_itinerary":[
{{"day":1,"pois":[{{"name":"place","time_window":"morning","cost_est_usd":5,"notes":"description"}}]}}
]
}}
"""
