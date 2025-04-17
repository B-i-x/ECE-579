# Humanized Viterbi implementation

import math

# set up hidden states and probs
states = ['Happy', 'Grumpy']
init_prob = {'Happy': 0.6, 'Grumpy': 0.4}
trans_prob = {
    'Happy': {'Happy': 0.8, 'Grumpy': 0.2},
    'Grumpy': {'Happy': 0.3, 'Grumpy': 0.7}
}
emit_prob = {
    'Happy':  {'purring': 0.6, 'ignoring': 0.3, 'hissing': 0.1},
    'Grumpy': {'purring': 0.1, 'ignoring': 0.4, 'hissing': 0.5}
}

# observations
obs = ['hissing', 'ignoring', 'ignoring', 'purring', 'purring']

# initialize structures
trellis = []
backptr = []

# initial step
trellis.append({})
backptr.append({})
for s in states:
    ln_init = math.log(init_prob[s])
    ln_emit = math.log(emit_prob[s][obs[0]])
    trellis[0][s] = ln_init + ln_emit  # first score
    backptr[0][s] = None               # no prev

# main loop
for t in range(1, len(obs)):
    trellis.append({})
    backptr.append({})
    for curr in states:
        best_prev = None
        best_score = float('-inf') # negative infinity for max search
        # check all previous
        for prev in states:
            score = trellis[t-1][prev] + math.log(trans_prob[prev][curr]) # transition prob
            if score > best_score:
                best_score = score
                best_prev = prev

        ln_emit = math.log(emit_prob[curr][obs[t]])
        trellis[t][curr] = best_score + ln_emit  # record
        backptr[t][curr] = best_prev             

# pick final and backtrack
final_state = max(states, key=lambda s: trellis[-1][s])
path = [final_state]
for t in range(len(obs)-1, 0, -1):
    prev = backptr[t][path[0]]
    path.insert(0, prev)

# print results
for idx, row in enumerate(trellis, start=1):
    print(f"t={idx}", row)
print("Most likely path:", path)
