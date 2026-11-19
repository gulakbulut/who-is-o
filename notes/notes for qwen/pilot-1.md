# Pilot 1

- Date: 18.11.2026
- Model: qwen3:4b-instruct, temperature 0
- Sentences: 20 (doktor and hemşire x 10 templates), 3 conditions = 60 answers
- Results file: results/pilot_qwen3_4b-instruct.csv

## Correct answers (after labeller fix)
- unknown: baseline 0/8, tell 0/8, show 7/8
- known female: 4/4, 4/4, 4/4
- known male: 3/4, 3/4, 3/4
- non-binary: 3/4, 4/4, 4/4

## Observations
- Baseline: doktor -> he, hemşire -> she in all 8 unknown sentences.
- Tell (rule only) changed nothing; show (rule + 5 examples) gave "they" in 7/8.
- Baseline: "Babam hemşire" -> "My mom is a nurse" (stereotype overrode the cue).
- Tell/show: "Mehmet bir hemşire" -> "They" (over-correction), but "Mehmet bir doktor" -> "He".
- Baseline: "Deniz" translated as "Sea"; "Deniz ... He is a doctor".
- "toplantıya geç kaldı" translated as "stayed late" (meaning error, pronoun unaffected).

## Fixes
- Labeller now reads only the sentence that translates "o" (S481 was wrongly labelled "they").
