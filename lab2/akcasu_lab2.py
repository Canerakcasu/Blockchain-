"""
Lab 2: Simulating Decentralized Agreement and Control
Course: Blockchain and its Application
Instructor: Vishnu Suresh
Student Script: akcasu_lab2.py
"""

print("=" * 60)
print("PART 1: Trust Model and Quorum Approval")
print("=" * 60)

# Step 1: Define the participants and proposal
validators = [
    "University A", "University B", "University C",
    "University D", "University E",
]
proposal = {
    "student": "Marta Kowalska",
    "credential": "Blockchain Fundamentals",
    "issuer": "University A",
}

# Step 2: Define the local validation rule
def validate_proposal(proposal):
    required = {"student", "credential", "issuer"}
    missing = required - set(proposal)
    if missing:
        return False, f"Missing fields: {sorted(missing)}"
    if proposal["issuer"] not in validators:
        return False, "Issuer is not a consortium member"
    return True, "Proposal follows the rules"

# Step 3: Collect votes and apply the quorum
def quorum_result(votes, threshold=4):
    approvals = sum(vote is True for vote in votes.values())
    responding = sum(vote is not None for vote in votes.values())
    return approvals >= threshold, approvals, responding

votes = {
    validator: validate_proposal(proposal)[0]
    for validator in validators
}

print("Votes:", votes)
print("Quorum result (Accepted, Approvals, Responding):", quorum_result(votes))


print("\n" + "=" * 60)
print("PART 2: Crash and Byzantine Faults")
print("=" * 60)

# Step 1: Simulate one crashed validator
crash_votes = votes.copy()
crash_votes["University E"] = None
print("Crash votes:", crash_votes)
print("Crash quorum result:", quorum_result(crash_votes))

# Step 2: Simulate one dishonest validator (maliciously rejects valid proposal)
dishonest_votes = votes.copy()
dishonest_votes["University E"] = False
print("\nDishonest votes:", dishonest_votes)
print("Dishonest quorum result:", quorum_result(dishonest_votes))

# Step 3: Submit an invalid proposal
invalid_proposal = {
    "student": "Marta Kowalska",
    "credential": "Blockchain Fundamentals",
    "issuer": "Unknown University",
}
invalid_votes = {
    validator: validate_proposal(invalid_proposal)[0]
    for validator in validators
}
invalid_votes["University E"] = True  # Dishonest approval
print("\nInvalid proposal votes:", invalid_votes)
print("Invalid proposal quorum result:", quorum_result(invalid_votes))


print("\n" + "=" * 60)
print("PART 3: Network Partitions Safety and Liveness")
print("=" * 60)

# Step 1: Test a three-two partition
def has_quorum(voter_set, threshold):
    return len(set(voter_set)) >= threshold

left_side = {"University A", "University B", "University C"}
right_side = {"University D", "University E"}

print("Left at threshold 4:", has_quorum(left_side, 4))
print("Right at threshold 4:", has_quorum(right_side, 4))

# Step 2: Lower the threshold and add equivocation
proposal_x_voters = {
    "University A", "University B", "University E"
}
proposal_y_voters = {
    "University C", "University D", "University E"
}

print("\nX at threshold 3:", has_quorum(proposal_x_voters, 3))
print("Y at threshold 3:", has_quorum(proposal_y_voters, 3))
print("Voted for both (Equivocating nodes):", proposal_x_voters & proposal_y_voters)


print("\n" + "=" * 60)
print("PART 4: Sybil Resistance")
print("=" * 60)

# Step 1: Count identities without membership control
def simple_majority(votes):
    approvals = sum(votes.values())
    return approvals > len(votes) / 2

honest_votes = {
    validator: False for validator in validators
}
fake_votes = {
    f"Fake identity {number}": True
    for number in range(1, 21)
}

open_votes = {**honest_votes, **fake_votes}
print("Identity count (Open):", len(open_votes))
print("Attacker wins (Open):", simple_majority(open_votes))

# Step 2: Apply permissioned membership
authorized = set(validators)
authorized_votes = {
    identity: vote
    for identity, vote in open_votes.items()
    if identity in authorized
}
print("\nAuthorized identities count:", len(authorized_votes))
print("Attacker wins (Permissioned):", simple_majority(authorized_votes))


print("\n" + "=" * 60)
print("PART 5: Effective Control and Unequal Voting Power")
print("=" * 60)

# Step 1: Add the coalition function
def minimum_coalition(weights, threshold):
    ordered = sorted(
        weights.items(), key=lambda item: item[1], reverse=True
    )
    coalition = []
    total = 0
    for validator, weight in ordered:
        coalition.append(validator)
        total += weight
        if total >= threshold:
            return coalition, total
    return coalition, total

# Step 2: Compare equal and concentrated power
equal_weights = {
    "A": 20, "B": 20, "C": 20, "D": 20, "E": 20
}
concentrated_weights = {
    "A": 40, "B": 25, "C": 15, "D": 10, "E": 10
}

print("Equal (threshold 67):", minimum_coalition(equal_weights, 67))
print("Concentrated (threshold 67):", minimum_coalition(concentrated_weights, 67))

# Step 3: Create an extreme case
extreme_weights = {
    "A": 70, "B": 10, "C": 10, "D": 5, "E": 5
}
print("Extreme (threshold 67):", minimum_coalition(extreme_weights, 67))
print("\nExplanation:")
print("Validator count alone fails to measure decentralization. In the extreme case,")
print("even though 5 validators exist, Validator A holds 70% of the voting weight,")
print("allowing it to unilaterally dictate consensus without any other validator.")
