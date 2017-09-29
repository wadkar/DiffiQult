import numpy as np
from Data import select_atom


class Getbasis:
    '''
    This class loads the basis
    '''
    def __init__(self,molecule,basis,shifted=False):
       # It is just a class for know, just in case we want to do more pre-procesing
       self.alpha = [] # exponents
       self.coef = []  # coef
       self.xyz = []   # coordinates of atoms
       self.l = []     # distribution of angular momentums
       self.list_contr = []
       self.tot_prim = 0
       if shifted:
          self.get_shiftedbasis(basis)
       else:
          self.get_centeredbasis(molecule,basis)
    
    def get_centeredbasis(self,molecule,basis):
       for atom in molecule:
          for contr in basis[atom[0]]:
              for l in self.getl_xyz(contr[0]): 
                  self.list_contr.append(len(contr[1]))
                  self.xyz.append([atom[1][0],atom[1][1],atom[1][2]])
                  self.l.append(l)
                  for prim in contr[1]:
                      self.alpha.append(prim[0])
                      self.coef.append(prim[1])
                      self.tot_prim += len(self.l[len(self.l)-1])

    def get_shiftedbasis(self,basis):
       for gauss in basis:
           self.alpha.append(gauss[1])
           self.coef.append(gauss[2])
           self.l.append(gauss[0])
           self.xyz.append(gauss[3])
       return

    def getl_xyz(self,l):
       angular = {'S':[(0,0,0)],
                  'P':[(1,0,0),(0,1,0),(0,0,1)]}
       return angular[l]


class Getgeom:
    '''
    This class loads the moleculegeom
    '''
    def __init__(self,molecule):
       self.xyz = []   # coordinates of atoms
       self.charge = []   # coordinates of atoms
       for atom in molecule:
          self.charge.append(int(atom[0]))
          self.xyz.append([atom[1][0],atom[1][1],atom[1][2]])
       return


class System_mol():
    '''This class contains all the information of the system
    extracted from mol and basis'''

    def __init__(self,mol,basis_set,ne,mol_name,angs=False,shifted=False):

          self.mol_name = mol_name
          ## Info for basis
          Basis = Getbasis(mol,basis_set,shifted=shifted)                        # Get basis
          self.list_contr = Basis.list_contr
          self.nbasis = len(Basis.list_contr)
          self.alpha = np.array(Basis.alpha)                                    # Alpha
          self.xyz = np.reshape(np.array(Basis.xyz,dtype='float64'),(self.nbasis,3)) # Nuclear coordinates
          self.l = Basis.l

          ## Geometry
          Geom = Getgeom(mol)                           # Get basis
          self.charges = np.array(Geom.charge)               # Charges
          self.atom = np.array(Geom.xyz)                     # Alpha
          self.natoms = len(self.charges)
   
          ## Normalization
          self.coef = np.array(Basis.coef)
  
          ## Number of electrons
          self.ne = ne
          if angs:
             factor = 0.529177249
             self.xyz = factor*self.xyz
             self.atom = factor*self.atom
          return

    def printcurrentgeombasis(self,tape):
       '''This method prints the current values of sys on tape'''
       ### Atom coordinates
       tape.write(' Atomic coordinates\n')
       for i,coord in enumerate(self.atom):
           line = '  '+select_atom.get(self.charges[i])
           line +=' '+str(i+1)+' '+str(self.charges[i])
           line +=' '+ str(coord[0])+' '+str(coord[1])+' '+str(coord[2]) + '\n'
           tape.write(line)
       
       tape.write(' Basis functions\n')
       ### Basis coordinates
       for i,coord in enumerate(self.xyz):
           line = '  '+str(i+1) 
           line +=' %2.6f %2.6f %2.6f'%(coord[0],coord[1],coord[2])
           if np.sum(self.l[i]) == 0 :
              line +=' s'
           else:
              line +=' p'
           line +=' %5.6f'%self.alpha[i]
           line +=' '+str(self.l[i][0]) +' '+str(self.l[i][1]) +' '+str(self.l[i][2]) +'\n'
           tape.write(line)
       tape.write('\n')
