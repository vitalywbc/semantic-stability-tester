# Semantic Stability Tester

A beginner Python project that checks whether repeated answers for the same
question are semantically stable.

The program:

- reads a text file of question IDs and answers
- groups answers by question ID with a dictionary
- counts how many times each answer appears
- calculates an SCI score for each question group
- computes the overall SCI score by averaging all question SCI scores
- draws a simple green/orange/red heatmap with canvas graphics
- prints the most unstable question groups

## Input Format

The data file uses one answer per line:

```text
question_id,answer
```

Example:

```text
Q1,yes
Q1,yes
Q1,yes
Q2,blue
Q2,green
Q2,blue
Q3,apple
Q3,orange
Q3,banana
Q3,apple
```

SCI means Semantic Consistency Index.

For each question group:

```text
question_sci = most_common_answer_count / total_answers * 100
```

Examples:

- `yes, yes, yes` = 100
- `blue, green, blue` = 66.67
- `apple, orange, banana, apple` = 50

Overall SCI is the average of all question SCI scores.

The heatmap colors are:

- green for SCI 80 or above
- orange for SCI 50 to 79
- red for SCI below 50

## Run

From this folder:

```bash
python3 semantic_stability_tester.py
```

Press Enter when asked for the file name to use `sample_answers.txt`.
