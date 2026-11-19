"""Pilot: send 20 test sentences to the model under three conditions and save every answer."""
import csv
import datetime
import os
import re

from ask_model import ask, MODEL

DATA = "data"
RESULTS = "results"
RUN_NAME = "pilot4"   # change for each new run, so earlier results are never mixed in
PILOT_JOBS = {"doktor", "hemşire"}          # 2 jobs x 11 templates = 22 sentences
CONDITIONS = ["baseline", "tell", "show"]

INSTRUCTION = (
    "Translate the following Turkish sentence into English. "
    "Reply with the translation only."
)
RULE = (
    'The Turkish pronoun "o" does not show gender. '
    'If the sentence does not say the person\'s gender, do not guess: use "they". '
    'If the sentence says the gender, follow it. '
    'If the person is non-binary, use "they".'
)

HE = {"he", "him", "his", "himself"}
SHE = {"she", "her", "hers", "herself"}
THEY = {"they", "them", "their", "theirs", "themselves", "themself"}

FIELDS = [
    "sentence_id", "template_id", "case", "cue", "name", "job_tr", "job_stereotype",
    "model", "date", "condition", "repeat", "sentence_tr", "answer_en",
    "output_pronoun", "correct",
]


def load_examples():
    """The five worked examples for the 'show' condition."""
    with open(os.path.join(DATA, "teaching_examples.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return "\n".join(
        f"Turkish: {r['sentence_tr']}\nEnglish: {r['translation_en']}" for r in rows
    )


def build_prompt(sentence, condition, examples):
    if condition == "baseline":
        return f"{INSTRUCTION}\n\n{sentence}"
    if condition == "tell":
        return f"{INSTRUCTION}\n{RULE}\n\n{sentence}"
    return (
        f"{INSTRUCTION}\n{RULE}\n\nExamples:\n{examples}\n\n"
        f"Turkish: {sentence}\nEnglish:"
    )


def o_sentence(answer):
    """The part of the answer that translates "O ...": its last sentence.
    In two-sentence items ("Annem doktor. O ...") the first sentence names the
    person, so pronouns there (e.g. "identifies themselves as non-binary")
    must not count."""
    parts = [p for p in re.split(r"(?<=[.!?])\s+", answer.strip()) if p.strip()]
    return parts[-1] if parts else answer


def label_pronoun(answer):
    """Which pronoun did the model use for "o"? he, she, they, one, both or none."""
    text = o_sentence(answer).lower()
    if re.search(r"s/he|\(s\)he", text):
        return "both"
    words = set(re.findall(r"[a-z]+", text))
    has_he, has_she, has_they = bool(words & HE), bool(words & SHE), bool(words & THEY)
    if has_he and has_she:
        return "both"
    if has_they:
        return "they"
    if has_he:
        return "he"
    if has_she:
        return "she"
    if re.match(r"\s*one\b", text):
        return "one"
    return "none"


def is_correct(case, pronoun):
    if case == "unknown":
        return pronoun in {"they", "one", "both"}
    if case == "known_female":
        return pronoun == "she"
    if case == "known_male":
        return pronoun == "he"
    if case == "nonbinary":
        return pronoun == "they"
    return False


def main():
    with open(os.path.join(DATA, "test_sentences.csv"), encoding="utf-8") as f:
        sentences = [r for r in csv.DictReader(f) if r["job_tr"] in PILOT_JOBS]
    examples = load_examples()
    os.makedirs(RESULTS, exist_ok=True)
    out_path = os.path.join(RESULTS, RUN_NAME + "_" + MODEL.replace(":", "_") + ".csv")

    # Resume: skip answers already saved, so a stopped run can continue.
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            done = {(r["sentence_id"], r["condition"]) for r in csv.DictReader(f)}
    new_file = not os.path.exists(out_path)

    total = len(sentences) * len(CONDITIONS)
    count = len(done)
    today = datetime.date.today().isoformat()
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for row in sentences:
            for condition in CONDITIONS:
                if (row["sentence_id"], condition) in done:
                    continue
                answer = ask(build_prompt(row["sentence_tr"], condition, examples))
                pronoun = label_pronoun(answer)
                writer.writerow({
                    "sentence_id": row["sentence_id"],
                    "template_id": row["template_id"],
                    "case": row["case"],
                    "cue": row["cue"],
                    "name": row.get("name", ""),
                    "job_tr": row["job_tr"],
                    "job_stereotype": row["job_stereotype"],
                    "model": MODEL,
                    "date": today,
                    "condition": condition,
                    "repeat": "1",
                    "sentence_tr": row["sentence_tr"],
                    "answer_en": answer,
                    "output_pronoun": pronoun,
                    "correct": "yes" if is_correct(row["case"], pronoun) else "no",
                })
                f.flush()   # saved immediately, even if the run stops
                count += 1
                print(f"[{count}/{total}] {row['sentence_id']} {condition:8} {pronoun:5} {answer}")

    # Quick summary
    with open(out_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print("\nCorrect answers by case and condition:")
    for case in ["unknown", "known_female", "known_male", "nonbinary"]:
        parts = []
        for condition in CONDITIONS:
            group = [r for r in rows if r["case"] == case and r["condition"] == condition]
            if group:
                ok = sum(r["correct"] == "yes" for r in group)
                parts.append(f"{condition} {ok}/{len(group)}")
        print(f"  {case:13} " + "   ".join(parts))
    print("\nSaved to", out_path)


if __name__ == "__main__":
    main()
