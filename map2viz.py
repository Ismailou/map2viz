from __future__ import with_statement
import re

class Section:
    def __init__(self, address, size, segment, section):
        self.address = address
        self.size = size
        self.segment = segment
        self.section = section
    def __str__(self):
        return self.section+""

class Symbol:
    def __init__(self, address, size, file, name):
        self.address = address
        self.size = size
        self.file = file
        self.name = name
    def __str__(self):
        return self.name

def get_line_number(phrase, file_name):
	with open(file_name) as f:
		for i, line in enumerate(f, 1):
			if phrase in line:
				return i
				
#===============================
# Load the Sections and Symbols
#
sections = []
symbols = []

if __name__ == "__main__":
	#linesList = open('C300_PCPU_APP_DEBUG_C1.map').readlines()
	f=open('C300_PCPU_APP_DEBUG_C1.map').readlines()
	in_sections = False
		
	for i, line in enumerate(f, 1):

		m = re.search('^(.text)', line)
		if m:
			in_sections = True
			#print m.group(1)
		
		if in_sections:
			if ('.text.' in line):
				#print i, ":", line 
				#print f[i]
	#			print re.split("\s+", line)
	#			entries = re.split("\s+", f[i]) 		
	#			print entries
	#			if (len(line) < 60 ):		
	#				print re.split("\s+", f[i+1])
				if ('0x' in line):
					# like  ".text.ScaleV   0x08006108       0x84 ./src/bsp/adc.o"
					# Or like  ".text.ADC_ttt  0x0800ffff       0xff ./system/src/stm32f0-stdperiph/stm32f0xx_adc.o
					#	                0x0800ffff                ADC_ttt"
					addr_size_module_entries = re.split("\s+", line);
					#print addr_size_module_entries[2], addr_size_module_entries[3], addr_size_module_entries[4], addr_size_module_entries[1].replace(".text.", "")
					symbols.append(Symbol(addr_size_module_entries[2], addr_size_module_entries[3], addr_size_module_entries[4], addr_size_module_entries[1].replace(".text.", "")))
				else:
					# like  .text.ADC_Init
					#                0x080041f4       0xd8 ./system/src/stm32f0-stdperiph/stm32f0xx_adc.o
					#                0x080041f4                ADC_Init
					
					# Or like  .text.ConnectADCChannel
					#                0x08006068       0xa0 ./src/bsp/adc.o
					addr_symbol_entries = re.split("\s+", line);
					addr_size_module_entries = re.split("\s+", f[i])
					#print addr_size_module_entries[1], addr_size_module_entries[2], addr_size_module_entries[3], addr_symbol_entries[1].replace(".text.", "")
					symbols.append(Symbol(addr_size_module_entries[1], addr_size_module_entries[2], addr_size_module_entries[3], addr_symbol_entries[1].replace(".text.", "")))

					
	for s in symbols:
		print s.address, s.size, s.file, s.name
					
				
    		
''' 	
		#print(line)
		m = re.search('^ (.text)', line)
		if m:
			print(line)
			print
			n = re.match('^.',line)
			print m,'-->', get_line_number(m.group(0),'C300_PCPU_APP_DEBUG_C1.map')
			if n:
				print(line)
#		if in_sections:
#			if in_sections:
#				sections.append(Section(eval(m.group(1)), eval(m.group(2)), m.group(3), m.group(5)))
#			else:
#				symbols.append(Symbol(eval(m.group(1)), eval(m.group(2)), m.group(3), m.group(5)))
#		else:
#			if len(sections) > 0:
#				in_sections = False


#===============================
# Gererate the HTML File
#
'''
'''
colors = ['9C9F84', 'A97D5D', 'F7DCB4', '5C755E']
total_height = 32.0

segments = set()
for s in sections: segments.add(s.segment)
segment_colors = dict()
i = 0
for s in segments:
    segment_colors[s] = colors[i % len(colors)]
    i += 1

total_size = 0
for s in symbols:
    total_size += s.size

sections.sort(lambda a,b: a.address - b.address)
symbols.sort(lambda a,b: a.address - b.address)

def section_from_address(addr):
    for s in sections:
        if addr >= s.address and addr < (s.address + s.size):
            return s
    return None

print "<html><head>"
print "  <style>a { color: black; text-decoration: none; font-family:monospace }</style>"
print "<body>"
print "<table cellspacing='1px'>"
for sym in symbols:
    section = section_from_address(sym.address)
    height = (total_height/total_size) * sym.size
    font_size = 1.0 if height > 1.0 else height
    print "<tr style='background-color:#%s;height:%gem;line-height:%gem;font-size:%gem'><td style='overflow:hidden'>" % \
        (segment_colors[section.segment], height, height, font_size)
    print "<a href='#%s'>%s</a>" % (sym.name, sym.name)
    print "</td></tr>"
print "</table>"
print "</body></html>"
'''
