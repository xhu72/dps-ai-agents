"""
Agent 1: Simple Reflex Vacuum-Cleaner Agent  

- Percept  : (location, status), e.g. ("A", "Dirty")
- Actions  : "Suck", "Left", "Right"
- Decision : condition-action rules applied to the CURRENT percept only.
             The agent stores nothing between steps (no memory).
"""

# ---------------------------------------------------------------------------
# The agent
# ---------------------------------------------------------------------------
class SimpleReflexVacuumAgent:
    """Chooses an action using only the current percept."""

    def is_dirty(self, loc, st):
        return st == "Dirty"

    def is_at_A(self, loc, st):
        return loc == "A"

    def is_at_B(self, loc, st):
        return loc == "B"

    def __init__(self):
        # Condition-action rules, checked in order.
        # Each rule = (description, condition function, action).
        self.rules = [
            ("status is Dirty -> Suck", self.is_dirty, "Suck"),
            ("location is A  -> Right", self.is_at_A, "Right"),
            ("location is B  -> Left", self.is_at_B, "Left"),
        ]

    def choose_action(self, percept):
        """Agent program: maps the current percept to an action."""
        location, status = percept
        for description, condition, action in self.rules:
            if condition(location, status):
                return action, description
        raise ValueError(f"No rule matches percept {percept}")


# ---------------------------------------------------------------------------
# The environment
# ---------------------------------------------------------------------------
class VacuumEnvironment:
    def __init__(self, status_A, status_B, agent_location):
        self.status = {"A": status_A, "B": status_B}
        self.agent_location = agent_location

    def percept(self):
        """What the agent's sensors report: (location, status)."""
        loc = self.agent_location
        return (loc, self.status[loc])

    def execute(self, action):
        """Actuators: apply the agent's action to the world."""
        if action == "Suck":
            self.status[self.agent_location] = "Clean"
        elif action == "Right":
            self.agent_location = "B"
        elif action == "Left":
            self.agent_location = "A"

    def clean_squares(self):
        count = 0
        for s in self.status.values():
            if s == "Clean":
                count += 1
        return count


# ---------------------------------------------------------------------------
# Run a simulation
# ---------------------------------------------------------------------------
def run(steps=5, status_A="Dirty", status_B="Dirty", start="A"):
    env = VacuumEnvironment(status_A, status_B, start)
    agent = SimpleReflexVacuumAgent()
    score = 0

    print("Start:", env.status, "| agent in", start)

    for step in range(1, steps + 1):
        percept = env.percept()                  # 1. sense
        action, rule = agent.choose_action(percept)  # 2. decide
        env.execute(action)                      # 3. act
        score += env.clean_squares()             # update score

        print("Step", step, "| saw", percept, "| did", action,
              "| world", env.status, "| score", score)
    print()


if __name__ == "__main__":
    for a in ["Clean", "Dirty"]:
        for b in ["Clean", "Dirty"]:
            for start in ["A", "B"]:
                run(steps=5, status_A=a, status_B=b, start=start)
