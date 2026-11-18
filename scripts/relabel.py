"""Re-label a results file with the current coding rules, without asking the model again.

Usage: python3 scripts/relabel.py results/pilot_qwen3_4b-instruct.csv
"""
import csv
import sys

from run_pilot import CONDITIONS, label_pronoun, is_correct


def main(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    changed = 0
    for r in rows:
        pronoun = label_pronoun(r["answer_en"])
        correct = "yes" if is_correct(r["case"], pronoun) else "no"
        if (pronoun, correct) != (r["output_pronoun"], r["correct"]):
            changed += 1
            print(f"{r['sentence_id']} {r['condition']:8} {r['output_pronoun']} -> {pronoun}   {r['answer_en']}")
        r["output_pronoun"], r["correct"] = pronoun, correct

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n{changed} label(s) changed.")

    print("\nCorrect answers by case and condition:")
    for case in ["unknown", "known_female", "known_male", "nonbinary"]:
        parts = []
        for condition in CONDITIONS:
            group = [r for r in rows if r["case"] == case and r["condition"] == condition]
            if group:
                ok = sum(r["correct"] == "yes" for r in group)
                parts.append(f"{condition} {ok}/{len(group)}")
        print(f"  {case:13} " + "   ".join(parts))


if __name__ == "__main__":
    main(sys.argv[1])
