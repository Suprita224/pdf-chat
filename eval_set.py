# Each entry: (question, [pages where the answer is]).
# If the answer appears on several pages, any of them counts as a correct hit.
# An empty list [] means the document does NOT answer the question (off-topic).
QUESTIONS = [
    ("What is the main question the project is trying to answer?", [2]),
    ("Why does the report say it is better to both make and resell bangles rather than do only one?", [2, 4]),
    ("What does gross margin mean?", [5]),
    ("Why should family members' unpaid work be counted as a cost?", [5, 8]),
    ("Which government support schemes does the report mention for new micro-enterprises?", [7, 8]),
    ("How should stock be bought for festival seasons so that cash is not tied up?", [7, 18, 23]),
    ("What details should be noted down when a supplier gives a price?", [12, 17, 30]),
    ("What precautions should be taken because bangles can break and leave sharp edges?", [16]),
    ("How much money is planned for starting and how is it divided between items?", [18, 19]),
    ("How is the selling price calculated from the cost and the margin the owner wants?", [18]),
    ("Is the estimated monthly surplus in the example a verified profit?", [19, 20]),
    ("What happens to the monthly surplus if materials cost a higher share of sales?", [22]),
    ("How can the team tell whether household income has doubled?", [20, 25]),
    ("What must the records show before the business grows beyond the trial?", [26]),
    ("How many people has the team spoken to in the field so far?", [3, 9]),
    ("What is the planned timeline for the first six months?", [21]),
    ("Where and when was the team photographed in the village?", [9]),
    # off-topic questions: the document cannot answer these
    ("Who won the 2018 football world cup?", []),
    ("What is the capital of France?", []),
    ("How do I install Python on Windows?", []),
    ("What is a good recipe for chicken biryani?", []),
]
