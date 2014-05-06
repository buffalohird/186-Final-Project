


# preferences:  n-dimensional array of preferences, e.g. preferences[10][5][10] = [1,2,1] means at prices $10, $5, $10, users prefer room 1, 2, and 1
def sperner(n, k, preferences, totalBalance):
  payments = list(xrange(0, totalBalance + 1, totalBalance / (k + 1)))
  paymentsLength = len(payments)

  allocations = reduceSperner(n, k+2, n, [], payments)

  allocations = startAllocations(allocations, n, k, payments)

  solutionSinks = [[0,0,2],[0,2,0],[2,0,0]]
  finalSolution = averageFair()



  print allocations





def createAllocations(allocations):
  return None


def reduceSperner(n, k, iterator, indices, payments):
  if iterator == 0:
    dollarSum = 0
    for index in indices:
      dollarSum += payments[index]
    if dollarSum != payments[len(payments) - 1]:
      return None
    return indices
  else:
    return [reduceSperner(n,k, iterator - 1, indices + [x], payments) for  x in xrange(k)]


def startAllocations(allocations, n, k, payments, iterator):
  if iterator == 0:









# bids: the values for each of n chores for the final triangle positions, e.g. [[1.0,2.0,1.0], [2.0,3.0,2.0],[4.0,3.0,3.0]]
def averageFair(n, bids):
  returnArray = []
  for bidder in xrange(n):
    values = bids[bidder]
    returnValue = sum(values) / len(values)
    returnArray.append(returnValue)
  return returnArray



def check_satisfying(choices):
  for choice in choices:
    choiceIndex = choice - 1
    if choices[choiceIndex] < 0:
      return False
    else:
      choices[choiceIndex] = -1 * choice
  return True


def get_neighbors(n, k, index):
  return None


def testInput():
  n, k = map(int, raw_input().split())
  preferences = [ [ [[0, 0, 3000], [1, 2, 3]], [[750, 0, 2250], [1, 2, 3]], [[1500, 0, 1500], [1, 2, 3]], [[2250, 0, 750], [1, 2, 3]], [] ], [ [], [], [], [], [] ], [ [], [], [], [], [] ], [ [], [], [], [], [] ], [ [], [], [], [], [] ] ]

  print n, k, preferences[0]



#print reduceSperner(2, 2, [[5,2,3],[4,3,2]], 1)

#print testInput()

print sperner(3, 1, [], 1000)






  
