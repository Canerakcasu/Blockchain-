# Step 1: Count identities without membership control
def simple_majority(votes):
    approvals = sum(votes.values())
    return approvals > len(votes) / 2

honest_votes = {validator: False for validator in validators}
fake_votes = {f"Fake identity {number}": True for number in range(1, 21)}

open_votes = {**honest_votes, **fake_votes}
print("Identity count:", len(open_votes))
print("Attacker wins (open):", simple_majority(open_votes))

# Step 2: Apply permissioned membership filtering
authorized = set(validators)
authorized_votes = {
    identity: vote
    for identity, vote in open_votes.items()
    if identity in authorized
}

print("\nAuthorized identities:", len(authorized_votes))
print("Attacker wins (filtered):", simple_majority(authorized_votes))