from . agents import *


class AgentDelta(Agent):
    
    def __init__(self,x = 2,y = 2):
        Agent.__init__(self)
        self.map = {(0,0): [True, True, True, True, 0]} #Nord, Sud, Ovest, Est, Parent
        self.pos = (0,0)
        self.fut = (0,0)
        self.curr = 'GoNorth'
        self.ritorna = True
		
		
        def program((status, bump)):

            def propagabump():
                coordnord = vector_add( (0,1), self.fut )
                coordsud = vector_add( (0,-1), self.fut )
                coordovest = vector_add( (-1,0), self.fut )
                coordest = vector_add( (1,0), self.fut )
                
                if coordnord in self.map:
                    self.map[coordnord][1] = False
                else:
                    self.map[coordnord] = [True, False, True, True, 9]

                if coordsud in self.map:
                    self.map[coordsud][0] = False
                else:
                    self.map[coordsud] = [False, True, True, True, 9]

                if coordovest in self.map:
                    self.map[coordovest][3] = False
                else:
                    self.map[coordovest] = [True, True, True, False, 9]
                    
                if coordest in self.map:
                    self.map[coordest][2] = False
                else:
                    self.map[coordest] = [True, True, False, True, 9]


            def propagaclean():
                coordnord = vector_add( (0,1), self.pos )
                coordsud = vector_add( (0,-1), self.pos )
                coordovest = vector_add( (-1,0), self.pos )
                coordest = vector_add( (1,0), self.pos )
                
                if coordnord in self.map:
                    self.map[coordnord][1] = False
                else:
                    self.map[coordnord] = [True, False, True, True, 9]

                if coordsud in self.map:
                    self.map[coordsud][0] = False
                else:
                    self.map[coordsud] = [False, True, True, True, 9]

                if coordovest in self.map:
                    self.map[coordovest][3] = False
                else:
                    self.map[coordovest] = [True, True, True, False, 9]
                    
                if coordest in self.map:
                    self.map[coordest][2] = False
                else:
                    self.map[coordest] = [True, True, False, True, 9]


            def gopadre(direzione):
                if direzione == 1:
                    self.pos = vector_add( (0,1), self.pos )
                    return 'GoNorth'
                elif direzione == 2:
                    self.pos = vector_add( (0,-1), self.pos )
                    return 'GoSouth'
                elif direzione == 3:
                    self.pos = vector_add( (-1,0), self.pos )
                    return 'GoWest'
                elif direzione == 4:
                    self.pos = vector_add( (1,0), self.pos )
                    return 'GoEast'
                
                
            def impostapadre():
                if self.curr == 'GoNorth':
                    self.map[self.fut][4] = 2
                elif self.curr == 'GoSouth':
                    self.map[self.fut][4] = 1
                elif self.curr == 'GoWest':
                    self.map[self.fut][4] = 4
                elif self.curr == 'GoEast':
                    self.map[self.fut][4] = 3

            
            def posizionefutura ():     
                if self.curr == 'GoNorth':
                    self.fut = vector_add( (0,1), self.pos )
                elif self.curr == 'GoSouth':
                    self.fut = vector_add( (0,-1), self.pos )
                elif self.curr == 'GoWest':
                    self.fut = vector_add( (-1,0), self.pos )
                elif self.curr == 'GoEast':
                    self.fut = vector_add( (1,0), self.pos )
                        
						
            def tagliaback ():                  
                if self.curr == 'GoNorth':
                    self.map[self.fut][1] = False
                if self.curr == 'GoSouth':
                    self.map[self.fut][0] = False
                if self.curr == 'GoWest':
                    self.map[self.fut][3] = False
                if self.curr == 'GoEast':
                    self.map[self.fut][2] = False
                
            
            def prossima ():                    
                if self.map[self.pos][0] == True:
                    self.curr='GoNorth'
                    self.map[self.pos][0] = False
                elif self.map[self.pos][1] == True:
                    self.curr='GoSouth'
                    self.map[self.pos][1] = False
                elif self.map[self.pos][2] == True:
                    self.curr='GoWest'
                    self.map[self.pos][2] = False
                elif self.map[self.pos][3] == True:
                    self.curr='GoEast'
                    self.map[self.pos][3] = False
                elif self.map[self.pos][4] != 0:
                    self.ritorna = True
                    self.curr = gopadre (self.map[self.pos][4])
                else:
                    self.curr = 'Noop'
            
			
	    #Main
            if self.curr == 'Noop':
                return 'Noop'

            posizionefutura()
            if status == 'Dirty': 
                return 'Suck'

            if bump == 'Bump':
                propagabump ()
                prossima ()
                return self.curr

                      
            if not self.ritorna:
			
                if not self.fut in self.map:
			self.map[self.fut] = [True, True, True, True, 0]
                impostapadre()
                tagliaback()
                self.pos = self.fut
                propagaclean ()
                prossima ()
                return self.curr
                
            else:
			
                self.ritorna = False
                prossima ()
                propagaclean ()
                return self.curr
            
        self.program = program
