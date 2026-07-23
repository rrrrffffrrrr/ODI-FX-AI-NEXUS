"""
ODI FX AI NEXUS

AI Signal Display
"""

import streamlit as st


def show_signal(signal, ai):
    """
    Displays the AI trade decision.
    """

    decision = ai.get("signal", "WAIT")

    if decision == "BUY":
        colour = "#00ff99"

    elif decision == "SELL":
        colour = "#ff4b4b"

    else:
        colour = "#ffc107"

    st.markdown(
        f"""
<div class="glass">

<h2 style="text-align:center;color:{colour};">
{decision}
</h2>

<hr>

<b>Trade Grade</b>

<h3>{ai.get("grade","A")}</h3>

<hr>

<b>Confidence</b>

<h2>{ai.get("confidence",0)}%</h2>

<hr>

<b>Entry Zone</b>

<p>
{ai.get("entry_low","-")}
&nbsp;&nbsp;to&nbsp;&nbsp;
{ai.get("entry_high","-")}
</p>

<hr>

<b>Stop Loss</b>

<p>{ai.get("sl","-")}</p>

<hr>

<b>Take Profit 1</b>

<p>{ai.get("tp1","-")}</p>

<b>Take Profit 2</b>

<p>{ai.get("tp2","-")}</p>

<b>Take Profit 3</b>

<p>{ai.get("tp3","-")}</p>

<hr>

<b>Risk : Reward</b>

<p>{ai.get("rr","-")}</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
<div class="glass">

<h3 style="color:#7CFCFF;">
🧠 AI Reasoning
</h3>

</div>
""",
        unsafe_allow_html=True,
    )

    reasons = ai.get("reasons", [])

    if len(reasons) == 0:

        st.info("AI reasoning unavailable.")

    else:

        for reason in reasons:

            st.success(reason)