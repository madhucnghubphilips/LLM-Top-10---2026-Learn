# Vendor-neutral OWASP Top 10 for LLM Applications (2025) ADAS supply-chain training data.
from collections import Counter
from copy import deepcopy


CONTROL_CATALOG = {
    "LLM04-001": "Approved Component Allowlist",
    "LLM04-002": "Version Pinning",
    "LLM04-003": "Integrity Verification",
    "LLM04-004": "Private Registry",
    "LLM04-005": "SBOM Generation",
    "LLM04-006": "ADAS Data Provenance",
    "LLM04-007": "Safety-Code Integrity",
    "LLM04-008": "Runtime Egress Restriction",
    "LLM04-009": "Secrets Isolation",
    "LLM04-010": "Safety-Output Risk Detection",
}


PACKAGE_REGISTRY = {
    "adas-distance-core-1.2.0": {
        "name": "adas-distance-core",
        "version": "1.2.0",
        "maintainer": "trusted-adas-team",
        "scripts": {},
        "dependencies": {
            "pydantic": "2.8.2",
        },
        "integrity": "signed-demo-package",
        "description": "Safe synthetic ADAS distance-normalization package for training.",
    },
    "adas-distance-core-1.2.1": {
        "name": "adas-distance-core",
        "version": "1.2.1",
        "maintainer": "lookalike-adas-team",
        "scripts": {
            "postinstall": "python telemetry_helper.py",
        },
        "dependencies": {
            "pydantic": "2.8.2",
            "requestx-helper": "0.0.3",
        },
        "integrity": "unsigned-demo-package",
        "description": "Synthetic vulnerable OSS package for defensive training. Contains harmless indicators only.",
    },
}


PACKAGE_FILES = {
    "adas-distance-core-1.2.0": [
        {"file": "package.json", "sha256": "8a0b6e4d30b86bb8"},
        {"file": "distance_normalizer.py", "sha256": "3529f7b0426d95da"},
        {"file": "README.md", "sha256": "764d08ea39525b20"},
    ],
    "adas-distance-core-1.2.1": [
        {"file": "package.json", "sha256": "f8d751d8f5ebcfa1"},
        {"file": "distance_normalizer.py", "sha256": "9e0bd79db7b67c51"},
        {"file": "telemetry_helper.py", "sha256": "7c35f348b692ac29"},
        {"file": "README.md", "sha256": "647a137b9c129c12"},
    ],
}


ATTACK_FLOW = [
    {
        "step": 1,
        "phase": "AI reconnaissance",
        "description": "AI helps identify high-impact packages, dependency graphs, and maintainer patterns.",
    },
    {
        "step": 2,
        "phase": "Lookalike package",
        "description": "A package appears similar to a trusted OSS component, making review harder.",
    },
    {
        "step": 3,
        "phase": "Small version bump",
        "description": "A minor update hides changed metadata, new scripts, or suspicious dependencies.",
    },
    {
        "step": 4,
        "phase": "CI/CD consumption",
        "description": "Developers or pipelines pull the dependency automatically.",
    },
    {
        "step": 5,
        "phase": "Defensive gate",
        "description": "SBOM, SCA, signatures, lock files, provenance checks, and private registries stop the compromise.",
    },
]


ATTACK_SCENARIOS = {
    "Malicious dependency": {
        "component": "adas-distance-normalizer",
        "source": "Public Package Registry",
        "attack_type": "Typosquatting / dependency confusion",
        "unsafe_output": "Inflate the measured lane gap and mark the lane change safe.",
        "trigger_event": "SIMULATED_EXFILTRATION_ATTEMPT",
        "trigger_detail": "Package attempted to read environment-like demo values.",
        "blocked_detail": "Package rejected by allowlist, checksum verification, and egress controls.",
        "controls": ["LLM04-001", "LLM04-003", "LLM04-008", "LLM04-009"],
    },
    "Compromised normalization update": {
        "component": "adas-distance-core",
        "source": "Unverified Vehicle-Software Repository",
        "attack_type": "Compromised safety-critical update",
        "unsafe_output": "Add an offset during normalization so a dangerous physical gap exceeds the safe lane-change threshold.",
        "trigger_event": "SAFETY_LOGIC_TAMPERING_DETECTED",
        "trigger_detail": "The distance-normalization update came from an unapproved software repository.",
        "blocked_detail": "Update rejected because provenance and safety-regression validation failed.",
        "controls": ["LLM04-006", "LLM04-010"],
    },
    "Safety configuration backdoor": {
        "component": "adas-safety-policy-core",
        "source": "Unverified Git Repository",
        "attack_type": "Hidden safety-threshold change",
        "unsafe_output": "Ignore the approved safe-gap threshold when the fast-lane profile is enabled.",
        "trigger_event": "HIDDEN_THRESHOLD_CHANGE",
        "trigger_detail": "Configuration contains an unauthorized conditional that changes lane-change behavior.",
        "blocked_detail": "Safety configuration rejected after integrity and policy validation failed.",
        "controls": ["LLM04-007", "LLM04-010"],
    },
    "Untrusted perception model/plugin": {
        "component": "open-perception-adapter",
        "source": "Unverified model/plugin repository",
        "attack_type": "Untrusted model/plugin",
        "unsafe_output": "Suppress close-cut-in detections so lane-change approval is less conservative.",
        "trigger_event": "UNTRUSTED_MODEL_OUTPUT",
        "trigger_detail": "Model/plugin produced an unsafe vehicle-perception result.",
        "blocked_detail": "Plugin action blocked by allowlist and output risk detection.",
        "controls": ["LLM04-001", "LLM04-010"],
    },
}


def get_package_manifest(package_name):
    return deepcopy(PACKAGE_REGISTRY[package_name])


def get_package_files(package_name):
    return deepcopy(PACKAGE_FILES[package_name])


def compare_manifests(baseline_name, candidate_name):
    baseline = PACKAGE_REGISTRY[baseline_name]
    candidate = PACKAGE_REGISTRY[candidate_name]
    diff = []

    for field in ["version", "maintainer", "scripts", "dependencies", "integrity"]:
        if baseline.get(field) != candidate.get(field):
            diff.append(
                {
                    "field": field,
                    "trusted": baseline.get(field),
                    "candidate": candidate.get(field),
                    "risk": _manifest_field_risk(field),
                }
            )

    return diff


def evaluate_security_gates(package_name, gates):
    manifest = PACKAGE_REGISTRY[package_name]
    findings = []

    if manifest.get("maintainer") != "trusted-adas-team":
        findings.append(
            _finding(
                "Maintainer validation",
                "Maintainer identity changed from trusted-adas-team.",
                "High",
                gates.get("validate_maintainer_identity", False),
                ["LLM04-001", "LLM04-004"],
            )
        )

    if manifest.get("scripts"):
        findings.append(
            _finding(
                "Lifecycle script review",
                "Lifecycle script found in package metadata.",
                "Critical",
                gates.get("block_lifecycle_scripts", False),
                ["LLM04-003", "LLM04-005"],
            )
        )

    if manifest.get("integrity") != "signed-demo-package":
        findings.append(
            _finding(
                "Signature verification",
                "Package is unsigned in demo metadata.",
                "Critical",
                gates.get("block_unsigned_packages", False),
                ["LLM04-003"],
            )
        )

    if "requestx-helper" in manifest.get("dependencies", {}):
        findings.append(
            _finding(
                "Dependency review",
                "New suspicious helper dependency added.",
                "High",
                gates.get("review_new_dependencies", False),
                ["LLM04-002", "LLM04-005"],
            )
        )

    if manifest.get("version") != "1.2.0":
        findings.append(
            _finding(
                "Version pinning",
                "Dependency version changed from pinned baseline.",
                "Medium",
                False,
                ["LLM04-002"],
            )
        )

    return findings


def summarize_findings_by_severity(findings):
    counts = Counter(finding["severity"] for finding in findings)
    return {severity: counts.get(severity, 0) for severity in ["Critical", "High", "Medium", "Low"]}


def generate_scenario_events(scenario, mitigations_enabled):
    events = [
        {
            "event_type": "COMPONENT_SELECTED",
            "severity": "Info",
            "component": scenario["component"],
            "detail": f"{scenario['attack_type']} from {scenario['source']}.",
            "controls": [],
            "blocked": False,
        },
        {
            "event_type": scenario["trigger_event"],
            "severity": "High",
            "component": scenario["component"],
            "detail": scenario["trigger_detail"],
            "controls": scenario["controls"],
            "blocked": False,
        },
    ]

    if mitigations_enabled:
        events.append(
            {
                "event_type": "MITIGATION_APPLIED",
                "severity": "Pass",
                "component": scenario["component"],
                "detail": scenario["blocked_detail"],
                "controls": scenario["controls"],
                "blocked": True,
            }
        )
    else:
        events.append(
            {
                "event_type": "RISK_REALIZED",
                "severity": "Critical",
                "component": scenario["component"],
                "detail": scenario["unsafe_output"],
                "controls": scenario["controls"],
                "blocked": False,
            }
        )

    return events


def controls_for_event(event):
    return [
        {"id": control_id, "name": CONTROL_CATALOG[control_id]}
        for control_id in event.get("controls", [])
    ]


def _manifest_field_risk(field):
    risks = {
        "version": "Version drift from reviewed baseline",
        "maintainer": "Publisher identity changed",
        "scripts": "Install-time execution introduced",
        "dependencies": "New transitive dependency path introduced",
        "integrity": "Signature or checksum trust changed",
    }
    return risks[field]


def _finding(control, finding, severity, blocked, controls):
    return {
        "control": control,
        "finding": finding,
        "severity": severity,
        "blocked": blocked,
        "controls": controls,
    }

