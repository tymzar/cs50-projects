from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
   Or(AKnight, AKnave),
   
    # Not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),

   
   Implication(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    # Not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),

    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),
    
    # A statement
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    # Not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),

    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),

    # A statement
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    
    # B statement
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave), And(BKnave, AKnight), And(BKnight, AKnave)  ))),
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave), And(BKnave, AKnight), And(BKnight, AKnave) ))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    
    # Not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),

    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),

    Biconditional(CKnight, Not(CKnave)),
    Biconditional(CKnave, Not(CKnight)),
    
    # A statement
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    
    # B statement
    Implication(AKnave, Not(BKnave)),
    Implication(AKnight, BKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, CKnave),
    
    # C statement
    Implication(CKnave, Not(AKnight)),
    Implication(CKnight, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
