'''
A simple table generator

file: https://gist.github.com/MayankFawkes/9c26882cea0fce086eeac689c418a0fa
'''

class Table:
	def __init__(self, titles:tuple, margin:int=0):
		self.titles = [n.upper() for n in titles]
		self.margin = margin
		self.width = len(titles)
		self.len = [len(title) for title in self.titles]
		self.tables = list()

	def _display(self):
		self.len = [n+self.margin for n in self.len]
		self.tables = [self.titles, *self.tables]
		tiles = [f"{'-'*n}" for n in self.len]
		tiles = "+".join(tiles)
		print(f"+{tiles}+")
		for n in range(len(self.tables)):
			r_display = list()
			for l, name in zip(self.len, self.tables[n]):
				r_display.append(f"{name or str('NA'):^{l}}")
			r_display = "|".join(r_display)
			print(f"|{r_display}|")
			print(f"+{tiles}+")


	def _mod_len(self, entries:tuple):
		count = 0 
		for past, new in zip(self.len, map(len, entries)):
			if past < new:
				self.len[count] = new
			count+=1

	def add_table(self, *entries:tuple):
		if len(entries) < len(self.titles):
			entries = [*entries, *["" for n in range(len(self.titles) - len(entries))]]
		self._mod_len(entries)
		self.tables.append(entries)

	def display(self):
		self._display()