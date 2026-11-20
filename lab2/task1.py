# Step 1: Define the participants and proposal
validators = [
    "University A",
    "University B",
    "University C",
    "University D",
    "University E",
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