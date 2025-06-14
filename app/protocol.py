from elGamal import ElGamal as eg
import os
import random

ips = [
    "192.168.0.1",
    "192.168.0.2",
    "192.168.0.3"
    ]

# user randomness
rand = [5234, 2865, 192381]

num_participants = 3
participants = [eg() for _ in range(num_participants)]

# Create group public key
group_public_key = 1
for participant in participants:
    group_public_key = (group_public_key * participant.y) % participants[0].p
    
for p in participants:
    p.setPK(group_public_key)

# Participants pick and encrypt indices
encrypted_indices = [p.encrypt(random.randint(1, num_participants)) for p in participants]

# Shuffle and re-encrypt the indices
num_shuffles = 3
for _ in range(num_shuffles):
    random.shuffle(encrypted_indices)
    encrypted_indices = [p.encrypt(ei[1]) for p in participants for ei in encrypted_indices]  # Ensure re-encrypting the second element of each tuple

# Blinding the indices
blinding_factors = [random.randint(1, participants[0].p - 1) for _ in participants]
blinded_indices = [p.blind(ei, bf) for p, ei, bf in zip(participants, encrypted_indices, blinding_factors)]

# Partial decryption by all participants
for p in participants:
    blinded_indices = [p.decShare(bi) for bi in blinded_indices]  # This should maintain tuples