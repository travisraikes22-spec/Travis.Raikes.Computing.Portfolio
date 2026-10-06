import json, random
from pathlib import Path

QUESTIONS=Path("questions.json")
SCORE=Path("highscore.json")

def load_questions():
    return json.loads(QUESTIONS.read_text(encoding="utf-8"))

def play():
    qs=load_questions(); random.shuffle(qs)
    categories=sorted(set(q["category"] for q in qs))
    print("Categories:", ", ".join(categories))
    chosen=input("Category (blank = all): ").strip().lower()
    if chosen: qs=[q for q in qs if q["category"].lower()==chosen]
    if not qs: print("No questions found."); return
    score=0
    for n,q in enumerate(qs,1):
        print(f"\n{n}. {q['question']}")
        for i,opt in enumerate(q["options"],1): print(f"  {i}) {opt}")
        try: ans=int(input("Answer: "))
        except ValueError: ans=0
        if ans==q["answer"]:
            score+=1; print("Correct!")
        else: print("Wrong —",q["options"][q["answer"]-1])
    print(f"\nFinal score: {score}/{len(qs)}")
    old=json.loads(SCORE.read_text()).get("highscore",0) if SCORE.exists() else 0
    if score>old:
        SCORE.write_text(json.dumps({"highscore":score},indent=2)); print("NEW HIGH SCORE!")

if __name__=="__main__":play()
