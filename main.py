#!/usr/bin/python

import random
import solver

# Rules
NUM_PEGS   = 4
NUM_COLORS = 6
SOLVER     = "elimination"
DEBUG      = True
# test

def createSolver( solverName ):
    if solverName == "brute":
        return solver.BruteSolver( NUM_PEGS, NUM_COLORS )
    elif solverName == "elimination":
        return solver.ColorEliminationSolver( NUM_PEGS, NUM_COLORS )
    elif solverName == "user":
        return solver.UserSolver( NUM_PEGS, NUM_COLORS )
    else:
        return solver.ColorEliminationSolver( NUM_PEGS, NUM_COLORS )


def evaluateGuess( guess, answer ):

    toReturn = ""

    ansRemainder      = []
    guessRemainder    = []

    # First evaluate blacks
    for idx, elt in enumerate( guess ):
        if elt == answer[idx]:
            # Add a match
            toReturn += "B"
        else:
            # Add to lists for white counting
            ansRemainder.append(answer[idx])
            guessRemainder.append( elt )

    # Then, evaluate whites
    for idx, elt in enumerate( guessRemainder ):
        if elt in ansRemainder:
            ansRemainder.remove(elt)
            toReturn += "W"

    return toReturn

def solve( solver, answer ):

    solved = False

    turn = 0

    while not solved:

        turn   = turn + 1
        guess  = solver.guess()
        if DEBUG: print guess

        result = evaluateGuess( guess, answer)
        if DEBUG: print result

        solver.computeResult( result )
        
        if result == 'B'*NUM_PEGS:
            solved = True
            print "Solved in %d turn(s)." % turn
            return turn


def runSolver( iterations ):

    turns = []
    count = 0

    while count < iterations:

        currSolver = createSolver( SOLVER )

        answer = [random.randint(1,NUM_COLORS) for x in xrange(NUM_PEGS)]
        print "Answer:" + str( answer )

        turns.append( solve( currSolver, answer ) )

        count += 1

    print "Avg turns: %f" % (sum(turns)/len(turns))

if __name__ == "__main__":
    runSolver( 10 )
