from app import answer_question

eval_cases=[
    {'question':'What is Atharva studyin?',"expect_keyword":'Computer Science'},
    {'question':'What projects Atharva Built?','expect_keyword':'Fraud'},
    {'question':'What programming language does Atharva have?','expect_keyword':'Python'},
    {'question':'Does Atharva Have a driving liscense','expect_keyword':None}
]

def run_eval():
    passed=0
    for case in eval_cases:
        answer,scores=answer_question(case['question'])
        expected=case['expect_keyword']

        if expected is None:
            ok="don't i have that information "in answer
        else:
            ok=expected.lower() in answer.lower()

        status="PASS" if ok else "FAIL"
        if ok:
            passed += 1

        print(f"[{status}] Q:{case['question']}")
        print(f"A:{answer}\n")

    print(f"Result:{passed}/{len(eval_cases)} passed")


if __name__ == "__main__":
    run_eval()












