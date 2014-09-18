#!/usr/bin/python

import random

# Rules
NUM_PEGS = 4
NUM_COLORS = 6
SOLVER = "elimination"


class Solver(object):
    """Solver template"""

    def __init__(self, pegs, colors):
        self.pegs = pegs
        self.colors = colors

    def guess(self):
        return [1,1,1,1]

    def computeResult( self, result ):
        pass



class UserSolver(object):
    """Prompt user for answer"""

    def __init__(self, pegs, colors):
        self.pegs = pegs
        self.colors = colors

    def guess(self):
        sol = raw_input("Your space-separated answer:")
        return map(int,sol.split(" "))

    def computeResult( self, result ):
        pass



class BruteSolver(Solver):
    """Solver for 4-peg, 6-color solutions"""

    counter = 0

    def __init__(self, pegs, colors):
        self.pegs = pegs
        self.colors = colors

    def guess(self):
        thisGuess = []
        for peg in xrange(0,self.pegs):
            thisGuess.append( ( (self.counter / self.colors**peg) % self.colors ) + 1 )

        return thisGuess

    def computeResult( self, result ):
        self.counter += 1



class ColorEliminationSolver(Solver):
    """Solves by first checking each color and then doing permutations"""

    def __init__(self, pegs, colors):
        self.pegs = pegs
        self.colors = colors
        
        # Current solver step
        self.guessType = "eliminate"
        self.guessStep = 1
        self.colorCount = {}

        self.permutations = []

    def guess(self):
        if self.guessType == "eliminate":
            return [self.guessStep for x in range(self.pegs)]
        elif self.guessType == "permute":
            return self.permutations[self.guessStep]

    def computeResult( self, result ):

        if self.guessType == "eliminate":
            self.colorCount[self.guessStep] = len(result)

            # All colors tried, color list complete, try permutations
            if self.guessStep == self.colors:
                self.guessType = "permute"
                # Build permutation tree
                # build a fucking huge list
                original = []
                for colorname,number in self.colorCount.iteritems():
                    original += [colorname]*number
                self.permutations = self.decompose( original, [] )
                self.guessStep = 0
            else:
                self.guessStep += 1

        elif self.guessType == "permute":
                self.guessStep += 1


    def decompose( self, decomposable, prefix ):

        if len(decomposable) == 2   :
            return [
            prefix + [decomposable[0], decomposable[1]],
            prefix + [decomposable[1], decomposable[0]]
            ]
        else:

            out  = []

            for el in decomposable:
                next = decomposable[:]
                next.remove(el)
                out += self.decompose( next, prefix + [el] )

            return out


#################################

def createSolver( solverName ):
    if solverName == "brute":
        return BruteSolver( NUM_PEGS, NUM_COLORS )
    elif solverName == "elimination":
        return ColorEliminationSolver( NUM_PEGS, NUM_COLORS )
    elif solverName == "user":
        return UserSolver( NUM_PEGS, NUM_COLORS )
    else:
        return ColorEliminationSolver( NUM_PEGS, NUM_COLORS )


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
        print guess
        result = evaluateGuess( guess, answer)
        print result
        solver.computeResult( result )
        if result == 'B'*NUM_PEGS:
            solved = True
            print "Solved in %d turn(s)." % turn
            return turn


def runSolver(iterations):

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
    runSolver(100)