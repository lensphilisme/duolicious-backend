import numpy as np

def compute_personality_vectors(
    new_presence_score,
    new_absence_score,
    old_presence_score,
    old_absence_score,
    cur_presence_score,
    cur_absence_score,
    cur_count_answers
):
    presence_score = np.array(cur_presence_score, dtype=np.int64)
    absence_score  = np.array(cur_absence_score, dtype=np.int64)
    count_answers  = cur_count_answers

    if new_presence_score and new_absence_score:
        excess = np.minimum(new_presence_score, new_absence_score)
        presence_score += np.array(new_presence_score) - excess
        absence_score  += np.array(new_absence_score) - excess
        count_answers  += 1

    if old_presence_score and old_absence_score:
        excess = np.minimum(old_presence_score, old_absence_score)
        presence_score -= np.array(old_presence_score) - excess
        absence_score  -= np.array(old_absence_score) - excess
        count_answers  -= 1

    numerator = presence_score
    denominator = presence_score + absence_score
    trait_percentages = np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, 0.5, dtype=np.float64),
        where=denominator != 0
    )

    ll = lambda x: np.log(np.log(x + 1) + 1)

    personality_weight = ll(count_answers) / ll(250)
    personality_weight = np.clip(personality_weight, 0, 1)

    personality = 2 * trait_percentages - 1
    personality = np.concatenate([personality, [1e-5]])
    personality /= np.linalg.norm(personality)
    personality *= personality_weight

    return (
        personality.tolist(),
        presence_score.tolist(),
        absence_score.tolist(),
        int(count_answers),
    )
