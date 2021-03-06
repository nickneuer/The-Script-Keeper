
import sqlite3 
import csv

conn = sqlite3.connect('Keith_Books.db')
c = conn.cursor()

TEXT = "select A.author, A.title, A.BISAC, A.TW-B.TW, (A.TW-B.TW)/A.RTD, A.isbn from {} A join {} B on A.isbn = B.isbn {} order by (A.TW-B.TW)/A.RTD desc limit 10"

COMPS = "(A.publisher like '%F%&%W%' or A.publisher like '%LIGHTNING%' or A.publisher like '%PGW%' or A.publisher like '%PERSEUS%' or A.publisher like '%NEW HARBINGER%' or A.publisher like '%SOURCE%' or A.isbn like '978157061%' or A.isbn like '978157062%' or A.isbn like '978159474%' or A.isbn like '978158394%') {}"

SPECIFIC_HOUSES = "(A.isbn like '978157061%' or A.isbn like '978157062%' or A.isbn like '978159474%' or A.isbn like '978158394%') {}"

RELIGION = "(A.BISAC like 'REL%') {} "

SELF_PUB = "(A.publisher like '%LIGHTNING%' or A.publisher like '%SOURCE%') {}"

HEALTH_N_DIET = "(A.BISAC = 'HEA010000' or A.BISAC = 'HEA019000' or A.BISAC = 'HEA017000') {}"

HEALTHY_COOKING = "(A.BISAC = 'CKB086000' or A.BISAC = 'CKB025000' or A.BISAC = 'CKB026000') {}"

FITNESS = "(A.BISAC = 'HEA007000') {}"

CRAFTING = "(A.BISAC like 'CRA%') {}"

class Flag(object):

  def __init__(self, later_week, earlier_week, refinement = '{}'):

    # refinement takes the form "(<normal text between where clause and order by> ) {}"     
    self.later_week = later_week
    self.earlier_week = earlier_week
    self.text = TEXT.format(later_week, earlier_week, refinement)   
    self.refinement = refinement 
    
  def comps(self):    
    return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + COMPS))  

  def spec_houses(self):    
    return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + SPECIFIC_HOUSES))

  def self_pub(self):    
    return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + SELF_PUB))

  def religion(self):   
    if COMPS in self.text or SELF_PUB in self.text or SPECIFIC_HOUSES in self.text: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('and ' + RELIGION))
    else: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + RELIGION))

  def health_n_diet(self):  
    if COMPS in self.text or SELF_PUB in self.text or SPECIFIC_HOUSES in self.text: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('and ' + HEALTH_N_DIET))
    else: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + HEALTH_N_DIET))

  def healthy_cooking(self):  
    if COMPS in self.text or SELF_PUB in self.text or SPECIFIC_HOUSES in self.text: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('and ' + HEALTHY_COOKING))
    else: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + HEALTHY_COOKING))

  def fitness(self):
    if COMPS in self.text or SELF_PUB in self.text or SPECIFIC_HOUSES in self.text: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('and ' + FITNESS))
    else: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + FITNESS))

  def crafting(self):
    if COMPS in self.text or SELF_PUB in self.text or SPECIFIC_HOUSES in self.text: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('and ' + CRAFTING))
    else: 
      return Flag(self.later_week, self.earlier_week, self.refinement.format('where ' + CRAFTING))

  def run_query(self):
    table = c.execute(self.text.format(''))
    for row in table:
      print row
  
  def write_table(self):
    table = c.execute(self.text.format(''))
    rows = [row for row in table]
    out_file = raw_input("choose out-file name")
    with open(out_file, "wb") as f:
      writer = csv.writer(f, delimiter = ',')
      writer.writerows(rows)

  def everything(self):
    return self
    
  competitors = [everything , comps, self_pub, spec_houses]

  genres = [everything, religion, health_n_diet, healthy_cooking, fitness, crafting]  

  
    
def run_all(weeks):
  # takes list of weeks, runs reports for all consecutive pairs   
  if type(weeks) != list and type(weeks) != tuple: 
    raise TypeError('arg of run_all must be a list or tuple')
  else:
    for i in range(1, len(weeks)):
      print ''
      print 'comparing ' + weeks[i] + ' to ' + weeks[i-1]
      print ''
      for f in Flag(weeks[i], weeks[i-1]).competitors:
        print f.__name__
        print '------------------------------------------------------------------------------------'
        for g in Flag(weeks[i], weeks[i-1]).genres:          
          print '     ' + g.__name__ + ':' 
          print ''
          g(f(Flag(weeks[i], weeks[i-1]))).run_query()
          print ''  



def write_all(weeks):
  # takes list of weeks, runs reports for all consecutive pairs 
  the_file = raw_input('choose name of file to write to')
  if type(weeks) != list and type(weeks) != tuple: 
    raise TypeError('arg of run_all must be a list or tuple')
  else:
    outfile = open(the_file, 'w')
    for i in range(1, len(weeks)):
      print >> outfile, ''
      print >> outfile, 'comparing ' + weeks[i] + ' to ' + weeks[i-1]
      print >> outfile, ''
      for f in Flag(weeks[i], weeks[i-1]).competitors:
        print >> outfile, f.__name__
        print >> outfile, '------------------------------------------------------------------------------------'
        for g in Flag(weeks[i], weeks[i-1]).genres:          
          print >> outfile, '     ' + g.__name__ + ':' 
          print >> outfile, ''
          rows = [row for row in c.execute(g(f(Flag(weeks[i], weeks[i-1]))).text.format(''))]            
          writer = csv.writer(outfile, delimiter = ',')
          writer.writerows(rows)                      
          print >> outfile, ''  
    outfile.close()


