from collections import deque
from dataclasses import dataclass, field
from typing import List
import random

# ==========================================
# PEAS AGENT MODEL
# ==========================================

PEAS = {
    "Performance": "Detect cheating accurately",
    "Environment": "Online Examination",
    "Actuators": ["Warning", "Flag Student", "Generate Report"],
    "Sensors": ["Face Count", "Phone Detection", "Gaze Direction"]
}

# ==========================================
# DATA MODELS
# ==========================================

@dataclass
class Violation:
    name: str
    penalty: int


@dataclass
class ExamSession:
    student_name: str
    violations: List[Violation] = field(default_factory=list)
    risk_score: int = 0

    def add_violation(self, name, penalty):
        self.violations.append(Violation(name, penalty))
        self.risk_score += penalty


# ==========================================
# RULE BASED REASONING (CO1)
# ==========================================

def rule_engine(face_count, phone_detected, gaze_direction):

    violations = []

    if face_count == 0:
        violations.append(("No Face Detected", 10))

    if face_count > 1:
        violations.append(("Multiple Faces Detected", 20))

    if phone_detected:
        violations.append(("Mobile Phone Detected", 30))

    if gaze_direction == "away":
        violations.append(("Looking Away", 15))

    return violations


# ==========================================
# CSP STYLE CONSTRAINT CHECKING (CO3)
# ==========================================

def check_constraints(face_count, phone_detected, gaze):

    constraints = []

    if face_count != 1:
        constraints.append("Constraint Failed: Exactly One Face Required")

    if phone_detected:
        constraints.append("Constraint Failed: No Mobile Phone Allowed")

    if gaze != "screen":
        constraints.append("Constraint Failed: Student Must Look At Screen")

    return constraints


# ==========================================
# BFS SEARCH (CO2)
# ==========================================

state_graph = {
    "NORMAL": ["WARNING"],
    "WARNING": ["SUSPICIOUS"],
    "SUSPICIOUS": ["CHEATING"],
    "CHEATING": []
}


def bfs(start, goal):

    queue = deque([[start]])
    visited = set()

    while queue:

        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:

            visited.add(node)

            for neighbor in state_graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return []


# ==========================================
# UTILITY FUNCTION (CO4)
# ==========================================

def utility_function(score):

    if score >= 50:
        return "CHEATING"

    elif score >= 20:
        return "SUSPICIOUS"

    else:
        return "NORMAL"


# ==========================================
# BAYESIAN STYLE PROBABILITY (CO5)
# ==========================================

def cheating_probability(score):

    if score < 20:
        return 0.20

    elif score < 50:
        return 0.60

    else:
        return 0.90


# ==========================================
# EXPLAINABILITY (CO6)
# ==========================================

def generate_explanation(session):

    print("\n===== EXPLANATION =====")

    if not session.violations:
        print("No violations detected.")
        return

    for v in session.violations:
        print(f"- {v.name}")

    print(f"\nRisk Score = {session.risk_score}")
    print(f"Decision = {utility_function(session.risk_score)}")


# ==========================================
# MAIN PROCTORING AGENT
# ==========================================

def run_exam():

    print("====================================")
    print("INTELLIGENT EXAM PROCTORING SYSTEM")
    print("====================================")

    student = input("Enter Student Name: ")

    session = ExamSession(student)

    print("\nSimulating Exam Monitoring...\n")

    # Simulated sensor readings
    face_count = random.choice([0, 1, 1, 1, 2])
    phone_detected = random.choice([True, False])
    gaze_direction = random.choice(["screen", "screen", "away"])

    print("Sensor Readings")
    print("----------------")
    print("Face Count:", face_count)
    print("Phone Detected:", phone_detected)
    print("Gaze Direction:", gaze_direction)

    # Rule Engine
    violations = rule_engine(
        face_count,
        phone_detected,
        gaze_direction
    )

    for name, penalty in violations:
        session.add_violation(name, penalty)

    # CSP Constraints
    failed_constraints = check_constraints(
        face_count,
        phone_detected,
        gaze_direction
    )

    # Utility Decision
    state = utility_function(session.risk_score)

    # Probability
    probability = cheating_probability(session.risk_score)

    # Search Path
    path = bfs("NORMAL", state)

    print("\n===== RESULTS =====")
    print("Student:", student)
    print("Risk Score:", session.risk_score)
    print("State:", state)
    print("Cheating Probability:", probability)

    print("\nState Transition Path:")
    print(" -> ".join(path))

    print("\nConstraint Analysis:")
    if failed_constraints:
        for c in failed_constraints:
            print(c)
    else:
        print("All Constraints Satisfied")

    generate_explanation(session)

    print("\n===== FINAL REPORT =====")
    print("Total Violations:", len(session.violations))
    print("Final Status:", state)


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    run_exam()