# =============================================================================
# Blockchain Lab 1 – Akcasu
# =============================================================================
# This script implements core blockchain concepts from scratch using only
# Python's standard library.  Run it with:
#
#   python akcasu_lab1.py
#
# Sections
# --------
#   Part 1 – SHA-256 Hashing
#   Part 2 – Block Structure & Chain Linkage
#   Part 3 – Chain Validation & Tamper Detection
#   Part 4 – Proof of Work Mining
#   Part 5 – Forking & Longest-Chain Selection
#   Extension – Transaction Validity Rules
# =============================================================================

import hashlib
import json
from copy import deepcopy

# ── Helpers ──────────────────────────────────────────────────────────────────

def separator(title: str) -> None:
    """Print a section header."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


# =============================================================================
# PART 1 – SHA-256 Hashing
# =============================================================================
# SHA-256 is a one-way cryptographic hash function.  Given any input string it
# always produces a fixed-length 256-bit (64 hex-character) digest.  Even a
# single character change produces a completely different output – a property
# called the *avalanche effect*.
# =============================================================================

def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest of a UTF-8 encoded string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


separator("Part 1 – SHA-256 Hashing")

transactions = [
    "Alice pays Bob 10",
    "Bob pays Carol 4",
    "Carol pays David 2",
]

print("\nTransaction → Hash")
print("-" * 60)
for tx in transactions:
    print(f"  {tx}")
    print(f"  {sha256_text(tx)}\n")

# Avalanche-effect demo
original = "Alice pays Bob 10"
changed  = "Alice pays Bob 11"   # only the amount differs by 1

print("Avalanche effect (one character change):")
print(f"  Original : {sha256_text(original)}")
print(f"  Changed  : {sha256_text(changed)}")


# =============================================================================
# PART 2 – Block Structure and Chain Linkage
# =============================================================================
# Each block contains:
#   - index          : position in the chain
#   - timestamp      : creation time (ISO 8601)
#   - transactions   : list of transaction strings
#   - previous_hash  : hash of the preceding block (links the chain together)
#   - nonce          : arbitrary number used for mining (starts at 0)
#   - hash           : SHA-256 digest of all the above fields
#
# The genesis block (index 0) uses a string of 64 zeros as its previous_hash
# because it has no predecessor.
# =============================================================================

def calculate_block_hash(block: dict) -> str:
    """Compute SHA-256 over all block fields except the stored hash."""
    data    = {k: v for k, v in block.items() if k != "hash"}
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return sha256_text(encoded)


def make_block(
    index: int,
    transactions: list,
    previous_hash: str,
    timestamp: str,
    nonce: int = 0,
) -> dict:
    """Create and return a new block dictionary with its hash computed."""
    block = {
        "index":         index,
        "timestamp":     timestamp,
        "transactions":  transactions,
        "previous_hash": previous_hash,
        "nonce":         nonce,
    }
    block["hash"] = calculate_block_hash(block)
    return block


def show_chain(blocks: list) -> None:
    """Print a summary row for each block in the chain."""
    for block in blocks:
        print(
            f"  Block {block['index']}"
            f" | Hash: {block['hash'][:12]}..."
            f" | Prev: {block['previous_hash'][:12]}..."
            f" | Nonce: {block['nonce']}"
        )


separator("Part 2 – Block Structure and Chain Linkage")

genesis = make_block(
    0,
    ["Course blockchain begins"],
    "0" * 64,
    "2026-10-01T09:00:00Z",
)

block_1 = make_block(
    1,
    ["Alice pays Bob 10", "Bob pays Carol 4"],
    genesis["hash"],
    "2026-10-01T09:01:00Z",
)

block_2 = make_block(
    2,
    ["Carol pays David 2"],
    block_1["hash"],
    "2026-10-01T09:02:00Z",
)

chain = [genesis, block_1, block_2]
print()
show_chain(chain)


# =============================================================================
# PART 3 – Chain Validation and Tamper Detection
# =============================================================================
# To verify the chain we check two things for every block:
#   1. Integrity  – recompute the hash and compare it with the stored value.
#   2. Linkage    – confirm that previous_hash matches the actual hash of the
#                   preceding block.
# If an attacker modifies a transaction they must also update that block's hash
# AND every subsequent block's previous_hash – practically impossible in a real
# distributed network.
# =============================================================================

def validate_chain(blocks: list) -> tuple:
    """Return (True, message) if the chain is intact, (False, reason) otherwise."""
    for position, block in enumerate(blocks):
        recalculated = calculate_block_hash(block)
        if block["hash"] != recalculated:
            return False, f"Block {position} has changed contents"
        if position > 0:
            if block["previous_hash"] != blocks[position - 1]["hash"]:
                return False, f"Block {position} has a broken previous-hash link"
    return True, "Chain is valid"


separator("Part 3 – Chain Validation and Tamper Detection")

print(f"\n  Original chain          : {validate_chain(chain)}")

# Tamper with block 1
tampered_chain = deepcopy(chain)
tampered_chain[1]["transactions"][0] = "Alice pays Bob 100"
print(f"  After tampering data    : {validate_chain(tampered_chain)}")

# Attacker patches only block 1's hash
tampered_chain[1]["hash"] = calculate_block_hash(tampered_chain[1])
print(f"  After re-hashing blk 1  : {validate_chain(tampered_chain)}")


# =============================================================================
# PART 4 – Proof of Work Mining
# =============================================================================
# Proof of Work forces miners to do computational work before adding a block.
# The rule: the block's hash must start with a certain number of zeros
# (the difficulty target).  Miners increment a counter called the *nonce* until
# a qualifying hash is found.  Higher difficulty → exponentially more attempts.
# =============================================================================

def mine_block(
    index: int,
    transactions: list,
    previous_hash: str,
    timestamp: str,
    difficulty: int = 3,
) -> tuple:
    """
    Increment nonce until the block hash starts with `difficulty` leading zeros.
    Returns (mined_block, attempts).
    """
    block = {
        "index":         index,
        "timestamp":     timestamp,
        "transactions":  transactions,
        "previous_hash": previous_hash,
        "nonce":         0,
    }
    target   = "0" * difficulty
    attempts = 0

    while True:
        attempts += 1
        digest = calculate_block_hash(block)
        if digest.startswith(target):
            block["hash"] = digest
            return block, attempts
        block["nonce"] += 1


separator("Part 4 – Proof of Work Mining")

mined_block, attempts = mine_block(
    3,
    ["David pays Erin 1"],
    chain[-1]["hash"],
    "2026-10-01T09:03:00Z",
    difficulty=3,
)

print(f"\n  Difficulty : 3 leading zeros")
print(f"  Attempts   : {attempts}")
print(f"  Nonce      : {mined_block['nonce']}")
print(f"  Hash       : {mined_block['hash']}")


# =============================================================================
# PART 5 – Forking and Longest-Chain Selection
# =============================================================================
# A fork occurs when two miners find valid blocks at the same height
# simultaneously.  Both branches are temporarily valid.  The network resolves
# the fork by adopting the *longest* chain – the one with the most accumulated
# proof of work.  Nodes on the shorter branch discard their blocks and switch.
# =============================================================================

separator("Part 5 – Forking and Longest-Chain Selection")

branch_a = deepcopy(chain)
branch_b = deepcopy(chain)

# Two competing blocks on top of the same parent (chain[-1])
block_a, attempts_a = mine_block(
    3, ["David pays Erin 1"],  branch_a[-1]["hash"],
    "2026-10-01T09:03:00Z", difficulty=3,
)
block_b, attempts_b = mine_block(
    3, ["David pays Frank 1"], branch_b[-1]["hash"],
    "2026-10-01T09:03:01Z", difficulty=3,
)

branch_a.append(block_a)
branch_b.append(block_b)

print(f"\n  Branch A validity : {validate_chain(branch_a)}")
print(f"  Branch B validity : {validate_chain(branch_b)}")

# Branch A grows one more block → becomes the preferred (longest) chain
block_a_2, _ = mine_block(
    4, ["Erin pays Grace 1"], branch_a[-1]["hash"],
    "2026-10-01T09:04:00Z", difficulty=3,
)
branch_a.append(block_a_2)

preferred = max([branch_a, branch_b], key=len)
print(f"\n  Preferred chain length : {len(preferred)}")
print()
show_chain(preferred)


# =============================================================================
# EXTENSION – Transaction Validity Rules
# =============================================================================
# Cryptographic validation (hash checks) only proves that block data has not
# changed.  It does NOT catch logically invalid transactions such as:
#   - Negative or zero amounts
#   - A sender paying themselves
#   - Malformed strings
# A separate rule-based validator is required for business logic.
# =============================================================================

def is_valid_transaction(tx: str) -> bool:
    """
    Validate the logical rules for a transaction string:
        '<Sender> pays <Receiver> <Amount>'
    Returns True only when:
      - The format is correct (exactly 4 tokens, second token is 'pays')
      - Amount is a positive number
      - Sender and receiver are different
    """
    try:
        parts = tx.split(" ")
        if len(parts) != 4 or parts[1] != "pays":
            return False
        sender, _, receiver, amount_str = parts
        amount = float(amount_str)
        if amount <= 0 or sender == receiver:
            return False
        return True
    except Exception:
        return False


separator("Extension – Transaction Validity Rules")

test_cases = [
    "Alice pays Bob 10",    # valid
    "Alice pays Bob -10",   # invalid: negative amount
    "Alice pays Alice 5",   # invalid: self-payment
    "Alice Bob 10",         # invalid: wrong format
    "Alice pays Bob 0",     # invalid: zero amount
]

print(f"\n  {'Transaction':<30} {'Logically Valid?'}")
print("  " + "-" * 48)
for tx in test_cases:
    print(f"  {tx:<30} {is_valid_transaction(tx)}")

# A block that is cryptographically intact but logically invalid
invalid_tx = "Alice pays Bob -10"
bad_block   = make_block(3, [invalid_tx], chain[-1]["hash"], "2026-10-01T09:05:00Z")
test_chain  = deepcopy(chain)
test_chain.append(bad_block)

print(f"\n  Cryptographic chain validation : {validate_chain(test_chain)}")
print(f"  Logical transaction validation : {is_valid_transaction(invalid_tx)}")

separator("Done")
print("\n  All parts completed successfully.\n")
