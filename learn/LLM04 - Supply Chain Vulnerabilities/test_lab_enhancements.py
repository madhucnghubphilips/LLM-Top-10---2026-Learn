# Vendor-neutral tests for the LLM04 ADAS supply-chain training lab.
from pathlib import Path

from lab_enhancements import (
    ATTACK_SCENARIOS,
    compare_manifests,
    evaluate_security_gates,
    generate_scenario_events,
    summarize_findings_by_severity,
)

LAB_DIR = Path(__file__).resolve().parent


def test_live_simulation_is_documented_as_fifteenth_challenge():
    app_text = (LAB_DIR / "app.py").read_text(encoding="utf-8")
    readme_text = (LAB_DIR / "README.md").read_text(encoding="utf-8")

    assert '"14. Final Fix Challenge"' in app_text
    assert '"15. Live Supply Chain Simulation"' in app_text
    assert "<b>Mode:</b> 15 guided steps" in app_text
    assert "15. Live Supply Chain Simulation" in readme_text


def test_live_simulation_challenge_does_not_render_an_mcq_prompt():
    app_text = (LAB_DIR / "app.py").read_text(encoding="utf-8")
    live_step = app_text.split('"15. Live Supply Chain Simulation"', maxsplit=1)[1].split("),", maxsplit=1)[0]

    assert "Which package should pass" not in live_step
    assert 'st.subheader("🧪 Interactive Check")' in app_text
    assert "if not is_live_simulation_step and step.quiz and step.options:" in app_text


def test_live_simulation_challenge_starts_with_simulation_ui():
    app_text = (LAB_DIR / "app.py").read_text(encoding="utf-8")

    assert "is_live_simulation_step = step.title == \"15. Live Supply Chain Simulation\"" in app_text
    assert "if not is_live_simulation_step:" in app_text
    assert app_text.index("render_live_supply_chain_simulation()") < app_text.index('st.subheader("🔎 Mini Scanner: Supply Chain Red Flags")')


def test_compare_manifests_flags_supply_chain_changes():
    diff = compare_manifests("adas-distance-core-1.2.0", "adas-distance-core-1.2.1")

    labels = {item["field"] for item in diff}

    assert "maintainer" in labels
    assert "scripts" in labels
    assert "dependencies" in labels
    assert "integrity" in labels


def test_security_gates_block_enabled_findings_only():
    findings = evaluate_security_gates(
        "adas-distance-core-1.2.1",
        {
            "block_unsigned_packages": True,
            "block_lifecycle_scripts": False,
            "validate_maintainer_identity": True,
            "review_new_dependencies": False,
        },
    )

    blocked = {finding["control"] for finding in findings if finding["blocked"]}
    unblocked = {finding["control"] for finding in findings if not finding["blocked"]}

    assert "Signature verification" in blocked
    assert "Maintainer validation" in blocked
    assert "Lifecycle script review" in unblocked
    assert "Dependency review" in unblocked


def test_risk_summary_counts_findings_by_severity():
    findings = evaluate_security_gates(
        "adas-distance-core-1.2.1",
        {
            "block_unsigned_packages": True,
            "block_lifecycle_scripts": True,
            "validate_maintainer_identity": True,
            "review_new_dependencies": True,
        },
    )

    summary = summarize_findings_by_severity(findings)

    assert summary["Critical"] == 2
    assert summary["High"] == 2
    assert summary["Medium"] == 1


def test_scenario_events_include_control_mapping_and_blocking_state():
    scenario = ATTACK_SCENARIOS["Compromised normalization update"]
    events = generate_scenario_events(scenario, mitigations_enabled=True)

    assert events[0]["event_type"] == "COMPONENT_SELECTED"
    assert events[-1]["event_type"] == "MITIGATION_APPLIED"
    assert events[-1]["blocked"] is True
    assert "LLM04-006" in events[-1]["controls"]

