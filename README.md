# who-is-o
Bachelor’s thesis: can open AI models be taught that the Turkish pronoun “o” is gender-neutral? Test sentences, chatbot script and Weka analysis.


## How to run 
``` 
ollama pull qwen3:4b-instruct 
python3 scripts/run_pilot.py 
python3 scripts/relabel.py results/pilot_qwen3_4b-instruct.csv 

``` 

## Status 
- [x] Test sentences: 600 Turkish sentences in three cases 
- [x] Chatbot script: open models through Ollama, temperature 0 
- [x] Pilot 1: 20 sentences × 3 conditions (see `notes/pilot-1.md`) 
- [ ] Coding rules 
- [ ] Full data collection 
- [ ] Analysis in Weka 
- [ ] Thesis report
