from eval_set import QUESTIONS
from search import search

K = 4  # how many chunks the search returns

hits = 0
hits_at_1 = 0
reciprocal_sum = 0.0
answerable = 0
answer_best = []
offtopic_best = []

for question, pages in QUESTIONS:
    results = search(question, k=K)
    best = results[0]["distance"]
    got = [r["page"] for r in results]

    if not pages:
        offtopic_best.append(best)
        print(f"[off-topic] best distance {best:.2f}   {question}")
        continue

    answerable += 1
    answer_best.append(best)
    rank = None
    for position, r in enumerate(results, start=1):
        if r["page"] in pages:
            rank = position
            break
    if rank:
        hits += 1
        reciprocal_sum += 1 / rank
        if rank == 1:
            hits_at_1 += 1
    status = f"found at rank {rank}" if rank else "MISSED"
    print(f"[{status}] expected {pages}, got {got}   {question}")

print()
print(f"Questions with an answer in the document: {answerable}")
print(f"Hit@{K}: {hits}/{answerable} = {hits / answerable:.0%}")
print(f"Hit@1:  {hits_at_1}/{answerable} = {hits_at_1 / answerable:.0%}")
print(f"MRR:    {reciprocal_sum / answerable:.2f}")
print()
print(f"Best distance, answerable questions: {min(answer_best):.2f} to {max(answer_best):.2f}")
if offtopic_best:
    print(f"Best distance, off-topic questions:  {min(offtopic_best):.2f} to {max(offtopic_best):.2f}")

from answer import MAX_DISTANCE

wrongly_refused = sum(1 for d in answer_best if d > MAX_DISTANCE)
wrongly_answered = sum(1 for d in offtopic_best if d <= MAX_DISTANCE)
print()
print(f"Refusal cutoff {MAX_DISTANCE}:")
print(f"  answerable questions wrongly refused: {wrongly_refused}/{len(answer_best)}")
print(f"  off-topic questions wrongly answered: {wrongly_answered}/{len(offtopic_best)}")
