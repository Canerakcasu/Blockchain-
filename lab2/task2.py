# Step 1: Simulate one crashed validator (stops responding)
crash_votes = votes.copy()
crash_votes["University E"] = None
print("Crash votes:", crash_votes)
print("Crash quorum:", quorum_result(crash_votes))

# Step 2: Simulate one dishonest validator (rejects a valid proposal)
dishonest_votes = votes.copy()
dishonest_votes["University E"] = False
print("\nDishonest votes:", dishonest_votes)
print("Dishonest quorum:", quorum_result(dishonest_votes))

# Step 3: Submit an invalid proposal with one malicious approval
invalid_proposal = {
    "student": "Marta Kowalska",
    "credential": "Blockchain Fundamentals",
    "issuer": "Unknown University",
}

invalid_votes = {
    validator: validate_proposal(invalid_proposal)[0]
    for validator in validators
}
# Malicious validator approves the invalid proposal
invalid_votes["University E"] = True

print("\nInvalid proposal votes:", invalid_votes)
print("Invalid proposal quorum:", quorum_result(invalid_votes))