# Step 1: Test a three-two partition with threshold 4
def has_quorum(voter_set, threshold):
    return len(set(voter_set)) >= threshold

left_side = {"University A", "University B", "University C"}
right_side = {"University D", "University E"}

print("Left at threshold 4:", has_quorum(left_side, 4))
print("Right at threshold 4:", has_quorum(right_side, 4))

# Step 2: Lower the threshold to 3 and add equivocation (contradictory votes)
proposal_x_voters = {"University A", "University B", "University E"}
proposal_y_voters = {"University C", "University D", "University E"}

print("\nX at threshold 3:", has_quorum(proposal_x_voters, 3))
print("Y at threshold 3:", has_quorum(proposal_y_voters, 3))
print("Voted for both:", proposal_x_voters & proposal_y_voters)