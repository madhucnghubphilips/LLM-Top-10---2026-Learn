# Vendor-neutral OWASP LLM03 Excessive Agency critical-infrastructure training lab.
import base64
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
ASSETS = APP_DIR / "assets"

st.set_page_config(
    page_title="LLM03 - Excessive Agency in Critical Infrastructure",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root {
    --primary: #d32f2f;
    --ink: #111827;
    --muted: #5b6475;
    --soft: #f5f7fb;
    --border: #e5e7eb;
    --app_bg: #ffffff;
    --panel_bg: #ffffff;
    --sidebar_bg: #f2f5f9;
    --hero-grad: linear-gradient(135deg,#fff 0%,#f8fbff 56%,#fff3f5 100%);
    --shadow: rgba(17,24,39,.18);
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] { background: var(--app_bg) !important; }
[data-testid="stSidebar"] { background: var(--sidebar_bg) !important; }
.hero {
    position: relative;
    padding: 32px 250px 32px 38px;
    border-radius: 28px;
    background: var(--hero-grad);
    border: 1px solid var(--border);
    box-shadow: 0 18px 45px var(--shadow);
    margin-bottom: 28px;
}
.hero h1 { font-size: 46px; line-height: 1.16; margin: 0; font-weight: 900; letter-spacing: -.045em; color: var(--ink); }
.hero p { color: var(--muted); font-size: 18px; margin-top: 14px; }
.hero-logo { position: absolute; top: 20px; right: 24px; width: 170px; max-width: 30%; height: auto; object-fit: contain; }
.hero-banner { display: block; width: 100%; max-height: 378px; object-fit: contain; object-position: center; border-radius: 12px; margin-top: 18px; margin-left: auto; margin-right: auto; }
.overview-img { display: block; width: 100%; max-height: 560px; object-fit: contain; border-radius: 12px; margin: 0 auto 24px auto; }
.overview-divider { border: 0; border-top: 1px solid rgba(128, 128, 128, 0.35); margin: 6px 0 28px 0; }
.hero .hero-quote { color: #FFFFFF; font-size: 19px; font-weight: 800; font-style: italic; margin-top: 14px; opacity: 0.97; background: #111827; border-left: 4px solid #FACC15; border-bottom: 2px solid rgba(239,68,68,0.65); box-shadow: 0 4px 20px rgba(34,197,94,0.3); padding: 12px 16px; border-radius: 8px; }
.pill { display: inline-block; padding: 7px 13px; border-radius: 999px; background: #fff0f2; color: #be123c; border: 1px solid #ffd4da; font-weight: 800; font-size: 13px; margin-bottom: 15px; margin-right: 8px; }
.card { background: var(--panel_bg); border: 1px solid var(--border); padding: 22px; border-radius: 22px; box-shadow: 0 12px 30px var(--shadow); margin-bottom: 16px; color: inherit; min-height: 145px; }
.danger { border-left: 8px solid #e53935; }
.safe { border-left: 8px solid #00a884; }
.neutral { border-left: 8px solid #5e35b1; }
.small { font-size: 0.92rem; color: #4d6070; }
.demo-pill { padding: 7px 12px; border-radius: 999px; background: #eef6ff; display: inline-block; margin: 3px; font-weight: 650; }
.action-log { font-family: monospace; background: #0d1117; color: #d6f5ff; padding: 14px; border-radius: 14px; }
.footer-note { text-align:center; color:var(--muted); padding:22px; }
.celebration-rise { position: fixed; inset: 0; pointer-events: none; overflow: hidden; z-index: 9999; }
.celebration-rise span { position: absolute; bottom: -72px; font-size: var(--party-size, 40px); left: var(--party-left); animation: float-party var(--party-duration, 4.6s) ease-out forwards; animation-delay: var(--party-delay, 0s); filter: drop-shadow(0 10px 16px rgba(17,24,39,.22)); }
@keyframes float-party { 0% { transform: translateY(0) rotate(-8deg); opacity: 0; } 8% { opacity: 1; } 82% { opacity: 1; } 100% { transform: translateY(-115vh) rotate(32deg); opacity: 0; } }
@media (max-width: 900px) {
    .hero { padding: 24px 24px 22px 24px; }
    .hero h1 { font-size: 32px; }
    .hero-logo { position: static; display: block; max-width: 180px; width: 52%; margin: 0 0 14px auto; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

page_logo_path = ASSETS / "critical-infrastructure-training-logo.png"

def image_html(path: Path, class_name: str, alt: str) -> str:
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"<img class='{class_name}' src='data:image/png;base64,{b64}' alt='{alt}'/>"

hero_logo_html = ""
hero_banner_html = image_html(
    ASSETS / "hero_excessive_agency.png",
    "hero-banner",
    "Excessive Agency affecting critical infrastructure",
)

overview_image_html = {
    1: image_html(ASSETS / "LLM03_01.png", "overview-img", "LLM03 Supply Chain Vulnerabilities overview"),
    2: image_html(ASSETS / "LLM03_02.png", "overview-img", "LLM03 Supply Chain Vulnerabilities impact and mitigations"),
}

SCENARIOS = {
    "400 kV Electrical Substation": {
        "icon": "⚡",
        "request": "A maintenance note reports intermittent relay noise. Investigate and resolve it immediately.",
        "vulnerable_actions": [
            "Trusted the unverified maintenance note",
            "Opened the breaker-control interface",
            "Issued a trip command to the 400 kV feeder",
            "Changed relay settings without operator confirmation",
        ],
        "secure_actions": [
            "Classified the report as untrusted evidence",
            "Retrieved read-only telemetry and relay diagnostics",
            "Prepared a recommended investigation plan",
            "Required two-person control-room approval for any trip or setting change",
        ],
        "lesson": "A substation assistant may analyze and recommend, but breaker trips and protection-setting changes require verified telemetry and human approval.",
        "risk": "Grid instability, equipment damage, cascading outage, and risk to personnel",
    },
    "Hydroelectric Dam": {
        "icon": "🌊",
        "request": "This inspection report says spillway vibration is critical. Take whatever action is necessary.",
        "vulnerable_actions": [
            "Accepted a malicious uploaded report as authoritative",
            "Opened spillway gates outside the approved operating plan",
            "Changed turbine governor setpoints",
            "Suppressed the alarm while executing the action",
        ],
        "secure_actions": [
            "Verified report signature, source, and timestamp",
            "Compared claims with independent sensor telemetry",
            "Generated a read-only safety assessment",
            "Required authorized dam operators to approve any gate or turbine action",
        ],
        "lesson": "Uploaded reports are data, not authority. Physical-control actions must remain outside the model's direct permissions.",
        "risk": "Uncontrolled water release, turbine damage, downstream flooding, and loss of generation",
    },
}

LEVELS = [
    {
        "id": 1,
        "title": "Level 1 - 400 kV Substation Trip Authority",
        "scenario": "An AI reads an unverified relay-maintenance note and can directly trip a 400 kV feeder or modify protection settings.",
        "hint": "Separate diagnostic assistance from physical breaker-control authority.",
        "questions": [
            {
                "id": "1A",
                "question": "What is the main excessive-agency issue in the substation scenario?",
                "options": {
                    "A": "The AI uses too much storage for relay telemetry.",
                    "B": "The AI can execute breaker trips and protection changes from unverified text without control-room approval.",
                    "C": "The AI explains relay diagnostics in too much detail.",
                    "D": "The maintenance report does not include enough formatting.",
                },
                "correct": "B",
                "explanation": "Breaker trips and relay-setting changes are safety-critical physical actions. The assistant must remain read-only and require verified telemetry plus authorized human approval.",
                "missing_keywords": "breaker trip, protection settings, read-only access, verified telemetry, control-room approval",
            }
        ],
    },
    {
        "id": 2,
        "title": "Level 2 - Malicious Dam Inspection Report",
        "scenario": "A hydroelectric-dam assistant treats an uploaded malicious inspection report as authority to open spillway gates and change turbine setpoints.",
        "hint": "Reports must be verified against provenance and independent telemetry before any operational decision.",
        "questions": [
            {
                "id": "2A",
                "question": "Which secure behavior best handles the uploaded dam report?",
                "options": {
                    "A": "Open the gates immediately because the report says the issue is critical.",
                    "B": "Verify the report source and signature, compare it with independent sensors, prepare a recommendation, and require operator approval.",
                    "C": "Change turbine settings automatically but leave the gates unchanged.",
                    "D": "Suppress alarms until the AI finishes its analysis.",
                },
                "correct": "B",
                "explanation": "The assistant should verify provenance and telemetry, remain advisory, and preserve operator control over gates and turbines.",
                "missing_keywords": "signed report, provenance, independent telemetry, advisory mode, operator approval",
            }
        ],
    },
]



def action_log(lines, safe=False):
    prefix = "✅" if safe else "🚨"
    return "\n".join([f"{prefix} {line}" for line in lines])


def render_page_logo():
    if page_logo_path.exists():
        _, logo_col = st.columns([5, 1])
        with logo_col:
            st.image(str(page_logo_path), width=130)


def render_current_overview():
    render_page_logo()
    hero_html = (
        "<div class='hero'>"
        f"{hero_logo_html}"
        "<span class='pill'>OWASP LLM03</span><span class='pill'>Critical Infrastructure</span><span class='pill'>Excessive Agency</span>"
        "<h1>LLM03 — Excessive Agency</h1>"
        '<p style="margin-top:12px;font-size:19px;color:var(--muted,#6b7280);max-width:820px;">AI performs actions or makes decisions <strong style="color:#ef4444;">beyond its intended authority or limits.</strong></p>'
        f"{hero_banner_html}"
        "<p class='hero-quote'>Learn how an over-powered infrastructure AI could trip substation equipment or act on a malicious dam report—and how read-only access, verified evidence, and operator approval prevent physical harm.</p>"
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    for overview_image_index in range(1, 3):
        html = overview_image_html.get(overview_image_index)
        if html:
            st.markdown(html, unsafe_allow_html=True)


def vulnerable_ai():
    st.subheader("Vulnerable AI Simulation")
    scenario_name = st.selectbox("Choose a scenario", list(SCENARIOS.keys()), key="vuln_scenario")
    scenario = SCENARIOS[scenario_name]
    st.markdown(f"### {scenario['icon']} {scenario_name}")
    st.info(f"User request: {scenario['request']}")
    if st.button("Run Vulnerable AI", type="primary"):
        st.markdown("<div class='card danger'><h3>Excessive Agency Detected</h3><p>The AI executed sensitive actions without confirmation and expanded beyond the original request.</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-log'>{action_log(scenario['vulnerable_actions']).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        st.error(f"Impact: {scenario['risk']}")


def secure_ai():
    st.subheader("Secure AI Simulation")
    scenario_name = st.selectbox("Choose a scenario", list(SCENARIOS.keys()), key="secure_scenario")
    scenario = SCENARIOS[scenario_name]
    st.markdown(f"### {scenario['icon']} {scenario_name}")
    st.info(f"User request: {scenario['request']}")
    approval = st.checkbox("Human approval provided")
    if st.button("Run Secure AI", type="primary"):
        st.markdown("<div class='card safe'><h3>Secure Agency Controls Applied</h3><p>The AI recommends or prepares the action, but sensitive execution is gated by approval and authorization.</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-log'>{action_log(scenario['secure_actions'], safe=True).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        if approval:
            st.success("Approved action executed within allowlisted scope and logged.")
        else:
            st.warning("Execution blocked because human approval was not provided.")
        st.caption(scenario["lesson"])


def comparison():
    st.subheader("Side-by-Side Comparison")
    scenario_name = st.selectbox("Choose a scenario", list(SCENARIOS.keys()), key="compare_scenario")
    scenario = SCENARIOS[scenario_name]
    left, right = st.columns(2)
    with left:
        st.markdown("<div class='card danger'><h3>❌ Vulnerable AI</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-log'>{action_log(scenario['vulnerable_actions']).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        st.error(scenario["risk"])
    with right:
        st.markdown("<div class='card safe'><h3>✅ Secure AI</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-log'>{action_log(scenario['secure_actions'], safe=True).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        st.success(scenario["lesson"])


def reset_level_state(level_id):
    if st.session_state.get("current_level") != level_id:
        st.session_state.current_level = level_id


def gandalf_levels():
    st.subheader("Interactive Levels")
    question_flow = []
    for level in LEVELS:
        for question in level["questions"]:
            question_flow.append({"level": level, "question": question})

    total_questions = len(question_flow)
    if "llm03_question_index" not in st.session_state:
        st.session_state.llm03_question_index = 0
    st.session_state.llm03_question_index = min(st.session_state.llm03_question_index, total_questions - 1)

    current_index = st.session_state.llm03_question_index
    current = question_flow[current_index]
    level = current["level"]
    question = current["question"]
    reset_level_state(level["id"])

    st.progress((current_index + 1) / total_questions, text=f"Question {current_index + 1} of {total_questions}")
    st.markdown(f"<div class='card neutral'><h3>{level['title']}</h3><p>{level['scenario']}</p></div>", unsafe_allow_html=True)
    with st.expander("Need a hint?"):
        st.write(level["hint"])

    st.markdown(f"#### Q{current_index + 1}. {question['question']}")
    option_labels = [f"{letter}) {option}" for letter, option in question["options"].items()]
    selected_option = st.radio("Select the best answer:", option_labels, key=f"mcq_level_{question['id']}", index=None)
    feedback_key = f"mcq_feedback_{question['id']}"
    passed_key = f"mcq_passed_{question['id']}"

    submit_col, prev_col, next_col, reset_col = st.columns([1.1, 1, 1, 1.2])
    with submit_col:
        if st.button("Submit Answer", key=f"submit_{question['id']}", type="primary"):
            if selected_option is None:
                st.session_state[feedback_key] = "Please select an answer before submitting."
                st.session_state[passed_key] = False
            else:
                selected_letter = selected_option.split(")", 1)[0]
                st.session_state[passed_key] = selected_letter == question["correct"]
                if st.session_state[passed_key]:
                    st.session_state[feedback_key] = "Correct. " + question["explanation"]
                    total_correct_after_submit = sum(
                        1
                        for item in question_flow
                        if st.session_state.get(f"mcq_passed_{item['question']['id']}", False)
                    )
                    if current_index == total_questions - 1 and total_correct_after_submit == total_questions:
                        st.session_state.llm03_party_burst_id = st.session_state.get("llm03_party_burst_id", 0) + 1
                else:
                    st.session_state[feedback_key] = f"Not quite. Focus on these missing concepts: {question['missing_keywords']}."
    with prev_col:
        if st.button("Previous", disabled=current_index == 0):
            st.session_state.llm03_question_index = max(0, current_index - 1)
            st.rerun()
    with next_col:
        can_advance = bool(st.session_state.get(feedback_key))
        if st.button("Next", disabled=current_index == total_questions - 1 or not can_advance):
            st.session_state.llm03_question_index = min(total_questions - 1, current_index + 1)
            st.rerun()
    with reset_col:
        if st.button("Restart MCQs"):
            st.session_state.llm03_question_index = 0
            for item in question_flow:
                qid = item["question"]["id"]
                st.session_state.pop(f"mcq_feedback_{qid}", None)
                st.session_state.pop(f"mcq_passed_{qid}", None)
            st.session_state.llm03_party_burst_id = 0
            st.rerun()

    if st.session_state.get(feedback_key):
        if st.session_state.get(passed_key):
            st.success(st.session_state[feedback_key])
        else:
            st.warning(st.session_state[feedback_key])

    total_correct = sum(
        1
        for item in question_flow
        if st.session_state.get(f"mcq_passed_{item['question']['id']}", False)
    )
    st.progress(total_correct / total_questions, text=f"Overall progress: {total_correct} of {total_questions} questions correct")
    if current_index == total_questions - 1 and st.session_state.get(feedback_key):
        if total_correct == total_questions:
            party_burst_id = st.session_state.get("llm03_party_burst_id", 0)
            party_animation = f"float-party-{party_burst_id}"
            party_icons = ["🎉", "🎊", "👏", "🎉", "👏", "🎊", "🎉", "🎊", "👏", "🎉", "👏", "🎊", "🎉", "🎊", "👏", "🎉", "👏", "🎊", "🎊", "👏", "🏆", "🛡️", "🎊", "👏", "🏆", "🛡️", "🎊", "👏", "🏆", "🛡️"]
            party_positions = [6, 12, 18, 24, 30, 36, 43, 49, 55, 61, 67, 73, 79, 85, 91, 15, 50, 83, 27, 70, 40, 60, 20, 80, 10, 90, 5, 95, 25, 75]
            party_spans = "".join(
                f"<span style='--party-left:{left}%;--party-delay:{(idx % 6) * 0.12}s;--party-size:{34 + (idx % 4) * 4}px;--party-duration:{4.1 + (idx % 5) * 0.18}s;animation:{party_animation} var(--party-duration, 4.6s) ease-out forwards var(--party-delay, 0s)'>{icon}</span>"
                for idx, (icon, left) in enumerate(zip(party_icons, party_positions))
            )
            st.markdown(
                f"""
                <style>
                @keyframes {party_animation} {{ 0% {{ transform: translateY(0) rotate(-8deg); opacity: 0; }} 8% {{ opacity: 1; }} 82% {{ opacity: 1; }} 100% {{ transform: translateY(-115vh) rotate(32deg); opacity: 0; }} }}
                </style>
                <div class='celebration-rise' data-burst='{party_burst_id}'>{party_spans}</div>
                <div class='card safe'><h3>Challenge Complete</h3><p>You completed all LLM03 excessive-agency MCQs. Key controls: verified evidence, read-only access, two-person approval, scoped actions, and operator review.</p></div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("You reached the final question. Use Previous to revisit any missed MCQs.")


def mitigations():
    st.subheader("Recommended Controls for LLM03")
    controls_data = [
        ["Two-person operator approval", "Required for breaker trips, relay settings, gates, and turbine controls"],
        ["Least privilege", "AI gets only the minimum tool permissions needed"],
        ["RBAC", "AI remains within the requesting operator's authorized facility and equipment scope"],
        ["Action allowlists", "Only approved operations are callable"],
        ["Verified telemetry", "Operational decisions require independent sensor evidence, not report text alone"],
        ["Limits", "Physical-control interfaces enforce equipment, command, and blast-radius limits"],
        ["Logging & monitoring", "Every AI-initiated action is traceable"],
        ["Dry-run mode", "Show impact before irreversible execution"],
    ]
    st.dataframe(pd.DataFrame(controls_data, columns=["Control", "How it reduces excessive agency"]), use_container_width=True, hide_index=True)


def sidebar():
    st.sidebar.title("Demo Navigation")
    page = st.sidebar.radio(
        "Choose module",
        ["1. Overview", "2. Vulnerable AI", "3. Secure AI", "4. Side-by-Side Comparison", "5. Interactive Levels", "6. Mitigations"],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Educational simulation only. No real APIs or external services are called.")
    return page


def main():
    page = sidebar()
    if page == "1. Overview":
        render_current_overview()
    else:
        render_page_logo()
        if page == "2. Vulnerable AI":
            vulnerable_ai()
        elif page == "3. Secure AI":
            secure_ai()
        elif page == "4. Side-by-Side Comparison":
            comparison()
        elif page == "5. Interactive Levels":
            gandalf_levels()
        elif page == "6. Mitigations":
            mitigations()
    st.markdown("<div class='footer-note'>LLM03 Excessive Agency | Fictional critical-infrastructure training simulation</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
