# Decisions

One entry per decision: what I decided, the options, my choice, why, and the date.

---

## Earlier decisions

### E1. Free open models instead of paid chatbots
- **Options:** paid chatbots (ChatGPT, Claude, Gemini) · free open models through Ollama
- **My choice:** free open models through Ollama
- **Why:** I want to write and run the chatbot script myself, without paying for a service.
- **Date:** 18 Nov 2026

### E2. Instruct model at temperature 0
- **Options:** qwen3:4b (thinking version) · qwen3:4b-instruct
- **My choice:** qwen3:4b-instruct, thinking off, temperature 0
- **Why:** the thinking version always wrote its reasoning before the translation (kept as test 2). Temperature 0 gives the same answer every time, so the results can be repeated.
- **Date:** 18 Nov 2026

### E3. Names that are also words
- **Options:** leave out names that are also words (Umut, Deniz) · include them like any name
- **My choice:** include them
- **Why:** they are used as first names just like Ayşe. Having a meaning doesn't make a name special.
- **Note:** if a model translates a name as a word (Deniz → "Sea"), I record it as a separate observation.
- **Date:** 19 Nov 2026

---

## Dataset v2 and the main study

### D1. Main contribution
- **Options:** 1 non-binary people in a genderless source language · 2 over-correction (erasing a stated gender) · 3 Turkish words for non-binary · 4 small free models
- **My choice:** 1 + 2 as the core, 3 + 4 as supporting points
- **Why:** earlier studies already show that AI guesses he/she for "o" and that training can reduce it. Keeping "o" open without erasing a stated gender or non-binary people hasn't been tested for Turkish.
- **Date:** 19 Nov 2026

### D2. Training
- **Options:** A prompts only · B add a "trained" condition · C training as future work
- **My choice:** B. Training is part of the thesis and will be done before finals, not left as future work.
- **How many models:** 2 models from different companies (see D8).
- **Why:** I want to teach the AI, not only test it, and compare teaching through the prompt with teaching through training on the same models.
- **Date:** 19 Nov 2026

### D3. Dataset
- **Options:** A my own set · B a ready-made set only · C combine
- **My choice:** A for the test set; C for the training set (my own new sentences + natural Turkish sentences from GATE X-E)
- **Why:** the test needs cases no ready-made set has (non-binary people, the known-gender control). Ready-made sentences make the training data more varied, and keeping them out of the test keeps the test fair.
- **Date:** 19 Nov 2026

### D4. Unisex names in the test
- **Options:** 2 (now) · 10 · 20
- **My choice:** 10
- **Why:** with 180 non-binary sentences, each name is used 18 times, so no single name decides the result. 10 clearly unisex names are easier to find and source than 20.
- **Rule:** names used in the teaching examples (Ege, Evren) or in the training set never appear in the test.
- **Date:** 19 Nov 2026

### D5. Names in the known-gender control
- **Options:** common · less common
- **My choice:** common names (e.g. from TÜİK's lists of the most given names)
- **Why:** here the name is the only gender cue, so the model must be able to know it. The unisex names in the non-binary sentences can be less common, so the model can't rely on what it already knows about a name.
- **Date:** 19 Nov 2026

### D6. Wording for non-binary
- **Options:** "non-binary" only · "ikili olmayan" only · both (· also "ikilik dışı")
- **My choice:** both "non-binary" and "ikili olmayan"
- **Why:** Turkish speakers use both. I want to see whether models understand the Turkish expression as well as the borrowed English word (contribution 3).
- **To do (Block 2):** v2 has two "non-binary" templates and one "ikili olmayan" template. Balance them so both get the same number of sentences.
- **Date:** 19 Nov 2026

### D7. Teaching examples in "show"
- **Options:** how many non-binary examples · whether to add a named known-gender example
- **My choice:** 2 non-binary examples + 1 named known-gender example, against over-correction
- **Why:** in pilot 1 the model turned "Mehmet bir hemşire" into "They". An example where a man has a job seen as female should show the model to follow the stated gender.
- **To do (Block 2):** the example must use a name and a job that are not in the test. Mehmet and hemşire both are.
- **Date:** 19 Nov 2026

### D8. Models
- **Options:** 2 × 8B on Colab · 4B on the Mac + one 8B · all three
- **My choice:** Qwen3 4B Instruct (Alibaba) + Gemma 3 4B (Google). Each is tested in all four conditions: baseline, tell, show, trained.
- **Why:** two different companies. Both can be trained on free Colab (Unsloth notebooks) and both run on my Mac before and after training. Aya Expanse has no Unsloth notebook, so it's dropped.
- **Date:** 19 Nov 2026
