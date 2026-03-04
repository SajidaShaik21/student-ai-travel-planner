
import streamlit as st
from planner import validate_inputs, build_prompt
from ai_client import AIClient
import pandas as pd

st.set_page_config(page_title="Student AI Travel Planner", layout="wide")

st.title("✈️ Student AI Travel Planner")


with st.form("planner_form"):

    destination = st.text_input("Destination")

    duration_days = st.number_input("Trip Duration",1,14,3)

    budget_level = st.selectbox("Budget Level",["tight","moderate","flexible"])

    transport = st.selectbox("Transport",["bus/train","shared cab","flight"])

    stay_type = st.selectbox("Stay Type",["hostel","homestay","budget hotel"])

    interests = st.text_input("Interests")

    currency = st.selectbox("Select Currency",["USD","INR"])

    submit = st.form_submit_button("Generate Travel Plan")


if submit:

    ok,msg,data = validate_inputs({

        "destination":destination,
        "duration_days":duration_days,
        "budget_level":budget_level,
        "transport":transport,
        "stay_type":stay_type,
        "interests":interests

    })


    if not ok:

        st.error(msg)

    else:

        st.info("Generating itinerary...")

        client = AIClient()

        system_prompt = "You are a helpful student travel planner."

        raw_output = client.chat_completion(system_prompt,build_prompt(data))

        parsed = client.extract_json_and_summary(raw_output)

        itinerary = parsed["itinerary_json"]

        days = itinerary.get("daily_itinerary",[])

        st.subheader("🧭 Travel Plan")

        costs = []

        for day in days:

            st.markdown(f"## 📅 Day {day['day']}")

            for poi in day["pois"]:

                cost = poi["cost_est_usd"]

                # Convert currency
                if currency == "INR":
                    cost_display = f"₹ {cost*83:.0f}"
                else:
                    cost_display = f"$ {cost}"

                st.markdown(f"""
                <div style="
                background:white;
                color:black;
                padding:18px;
                border-radius:12px;
                margin-bottom:12px;
                box-shadow:0px 3px 10px rgba(0,0,0,0.15);
                font-size:16px;
                ">

                <div style="font-size:20px;font-weight:bold;">
                📍 {poi['name']}
                </div>

                <br>

                ⏰ <b>Time:</b> {poi['time_window']}<br>
                💰 <b>Cost:</b> {cost_display}<br><br>

                📝 {poi['notes']}

                </div>
                """, unsafe_allow_html=True)

                costs.append({
                    "Place":poi["name"],
                    "Cost":cost if currency=="USD" else cost*83
                })


        if costs:

            df = pd.DataFrame(costs)

            st.subheader("💰 Budget Breakdown")

            st.bar_chart(df.set_index("Place"))
