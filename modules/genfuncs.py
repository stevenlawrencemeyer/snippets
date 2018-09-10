class GenFuncs():
	
	def __init__(self, pickle, os, datetime, sys):
		self.pickle = pickle
		self.os = os
		self.datetime = datetime
		self.sys = sys
		

	def write_to_pickle(self, fname, in_obj, max_tries):
		
		for try_nbr in range(max_tries):
			try:
				print('try_nbr= ' + str(try_nbr))
				fobj = open(fname, 'wb')
				self.pickle.dump(in_obj, fobj)
				fobj.close()
				break
			except Exception as e:
				print(type(e))
				print(e.args)
				print(e)
				if try_nbr >= max_tries - 1:
					print('You maxed out your tries')
					print('exiting from GF.write_to_pickle')
					self.sys.exit()

	def read_from_pickle(self, fname, max_tries):
		
		for try_nbr in range(max_tries):
			print('try_nbr= ' + str(try_nbr))
			try:
				fobj = open(fname, 'rb')
				out_obj = self.pickle.load(fobj)
				fobj.close()
				return out_obj
			except Exception as e:
				print(type(e))
				print(e.args)
				print(e)
				if try_nbr >= max_tries - 1:
					print('You maxed out your tries')
					print('Exiting from GF.read_from_pickle')
					self.sys.exit()

	def cleanse_str(self, cleansed_allowed, instr):
		#change to upper case
		instr = instr.upper()
		#remove leading definite article
		if len(instr) >= 4:
			if instr[:4] == 'THE ':
				instr = instr[4:]
		#remove disallowed chars
		outstr = ''
		n = len(instr)
		for i in range(n):
			if instr[i] in cleansed_allowed:
				outstr+= instr[i]
		return outstr		
				
		





