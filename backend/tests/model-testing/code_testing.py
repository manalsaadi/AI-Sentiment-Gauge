import re

# Read ground truth
with open("test_output.txt", "r", encoding="utf-8") as f:
    gt_lines = [line.strip() for line in f if line.strip()]
ground_truth = []
for line in gt_lines:
    if '\t' in line:
        comment, sentiment = line.rsplit('\t', 1)
        ground_truth.append((comment.strip(), sentiment.strip().lower()))
    else:
        *comment, sentiment = line.rsplit(" ", 1)
        ground_truth.append((" ".join(comment), sentiment.lower()))


# Parse report.md for sentiment results
with open("reports/report.md", "r", encoding="utf-8") as f:
    report = f.read()


# Extract predicted sentiment for each comment from the table in the report
sentiment_map = {}
table_pattern = re.compile(r"\| *Comment *\| *Predicted Sentiment *\|\n\|[-| ]+\|\n((?:\|.*\|\n)+)")
table_match = table_pattern.search(report)
if table_match:
    table_rows = table_match.group(1).strip().splitlines()
    for row in table_rows:
        # Each row: | comment | sentiment |
        parts = [cell.strip() for cell in row.strip().strip('|').split('|')]
        if len(parts) == 2:
            sentiment_map[parts[0]] = parts[1].lower()

# Compare
correct = 0
total = len(ground_truth)
unmatched = []
for comment, true_sentiment in ground_truth:
    detected = sentiment_map.get(comment)
    if detected == true_sentiment:
        correct += 1
    else:
        unmatched.append((comment, true_sentiment, detected))

accuracy = correct / total * 100 if total else 0
print(f"\nAccuracy: {accuracy:.2f}%")
if unmatched:
    print("\nUnmatched Sentiments:")
    for comment, true_sentiment, detected in unmatched:
        print(f"Comment: {comment}\n  Ground Truth: {true_sentiment}\n  Detected: {detected}")