import random

class Sperner:

  # preferences:  n-dimensional array of preferences, e.g. preferences[10][5][10] = [1,2,1] means at prices $10, $5, $10, users prefer room 1, 2, and 1
  def sperner(self, n, k, preferences, totalBalance):
    payments = list(xrange(0, totalBalance + 1, totalBalance / (k + 1)))
    paymentsLength = len(payments)
    self.agentPreferences = preferences
    allocations = self.createGraph(n, k+2, n, [], payments)

    """
    for i in allocations:
      for j in i:
        print j
      print "\n"
    """

    solutionSinks = self.solve(n, k + 2, allocations)#[[0,0,2],[0,2,0],[2,0,0]]
    if solutionSinks == None:
      return
    #print solutionSinks
    finalSolution = self.averageFair(n, solutionSinks, payments)
    return finalSolution


  def createGraph(self, n, k, iterator, indices, payments):
    allocations = [[[0 for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(k)]

    # create corners
    allocations[k - 1][0][0] = self.assignAgentToRoom([2], [k-1, 0, 0], n)
    allocations[0][k - 1][0] = self.assignAgentToRoom([3], [0, k-1, 0], n)
    allocations[0][0][k - 1] = self.assignAgentToRoom([1], [0, 0, k-1], n)

    # create edges
    for i in xrange(k):
      for j in xrange(k):
        allocations[i][j][0] = self.assignAgentToRoom([3], [i, j, 0], n)

    for j in xrange(k):
      for l in xrange(k):
        allocations[0][j][l] = self.assignAgentToRoom([1], [0, j, l], n)

    for i in xrange(k):
      for l in xrange(k):
        allocations[i][0][l] = self.assignAgentToRoom([2], [i, 0, l], n)

    # randomly "color" rest of graph
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          if payments[i] + payments[j] + payments[l] != payments[len(payments) - 1]:
            allocations[i][j][l] = None
          elif allocations[i][j][l] == 0: 
            allocations[i][j][l] = self.assignAgentToRoom([1,2,3], [i, j, l], n)

    return allocations


      
  def assignAgentToRoom(self, room, costs, n):
    agentPreferences = [self.agentPreferences[x][costs[0]][costs[1]][costs[2]] for x in xrange(n)]
    for preference in agentPreferences:
      if preference in room:
        return agentPreferences.index(preference) + 1

    return 40

  def generatePreferences(self, n, k):
    preferences = [[[[0 for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(n)]
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          for x in xrange(n):
            preferences[x][i][j][l] = random.randrange(1, n + 1)

    return preferences

  def solve(self, n, k, allocations):
    remaining, sinks, allocation = [], [], []
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          #print allocations[i][j][l], i, j, l
          if allocations[i][j][l] == None:
            continue
          if allocations[i][j][l] == 40:
            return None
          remaining = list(xrange(1, n + 1))
          sinks = []
          
          remaining.remove(allocations[i][j][l])
          sinks.append([i,j,l])
          neighbors = self.getNeighbors(i, j, l, k, allocations)
          
          for neighbor in neighbors:
            if neighbor[0] in remaining:
              remaining.remove(neighbor[0])
              sinks.append(neighbor[1])

    if len(remaining) == 0:
      return sinks
    else:
      print "no solution found for 3-person Sperner's"
      return None




  def averageFair(self, n, sinks, payments):
    returnArray = []
    for bidder in xrange(n):
      values = sinks[:][bidder]
      returnValue = sum([payments[x] for x in values]) / len(values)
      print returnValue
      returnArray.append(returnValue)
    return returnArray



  def check_satisfying(self, choices):
    for choice in choices:
      choiceIndex = choice - 1
      if choices[choiceIndex] < 0:
        return False
      else:
        choices[choiceIndex] = -1 * choice
    return True


  def getNeighbors(self, i, j, l, k, allocations):
    neighbors = [[i+ 1, j-1, l], [i-1, j+1, l], [i, j-1, l+1], [i, j+1, l-1],  [i-1, j, l+1], [i+1, j, l-1]] 
    for neighbor in neighbors:
      for index in neighbor:
        if index < 0 or index > k:
          neighbors.remove(neighbor)
          continue
    return [[allocations[x][y][z], [x,y,z]] for [x,y,z] in neighbors]


  def testInput(self):
    return True



#print reduceSperner(2, 2, [[5,2,3],[4,3,2]], 1)

#print testInput()

newSperner = Sperner()
preferences = newSperner.generatePreferences(3, 3)

print newSperner.sperner(3, 1, preferences, 1000)






  
