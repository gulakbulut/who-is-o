# First test w Gemma

- Date:19.11.26
- Model: gemma
- Command: time python3 scripts/run_pilot.py

- Qwen ignores the rule for unknown gender (tell 0/8) and only learns from examples.
- Gemma obeys the rule too much. Under tell, everyone becomes “they”, even “My father is a doctor. They work very hard.” That’s the “always they” over-correction your control group was designed to catch. Looking only at the neutral rate, Gemma would seem perfect (8/8). Your control accuracy shows that’s not learning, just a new default. That supports contribution 2 and shows why you need the control group.
- At baseline, Gemma ignores a stated non-binary identity, even with the English word: “Deniz is non-binary. He is a doctor.” So for Gemma, “non-binary” and the Turkish phrase do equally badly at baseline (0/4 each). For Qwen the English word helped (3/4). Contribution 3 seems to depend on the model, which is worth a sentence in Discussion.
- Names as words again: Devrim → “Revolution”, and Deniz and Bilge dropped entirely (“He/She is…”, “She is someone…”).