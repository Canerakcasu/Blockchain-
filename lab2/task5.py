# Step 1: Add the coalition function to find minimum coalition reaching threshold
def minimum_coalition(weights, threshold):
    ordered = sorted(weights.items(), key=lambda item: item[1], reverse=True)
    coalition = []
    total = 0
    for validator, weight in ordered:
        coalition.append(validator)
        total += weight
        if total >= threshold:
            return coalition, total
    return coalition, total

# Step 2: Compare equal and concentrated power (threshold = 67)
equal_weights = {
    "A": 20, "B": 20, "C": 20,
    "D": 20, "E": 20
}

concentrated_weights = {
    "A": 40, "B": 25, "C": 15,
    "D": 10, "E": 10
}

print("Equal:", minimum_coalition(equal_weights, 67))
print("Concentrated:", minimum_coalition(concentrated_weights, 67))

# Step 3: Create an extreme case (Validator A = 70, remaining 30 divided among others)
extreme_weights = {
    "A": 70, "B": 10, "C": 10,
    "D": 5, "E": 5
}

print("Extreme:", minimum_coalition(extreme_weights, 67))