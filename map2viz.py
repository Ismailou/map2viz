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

def addr_in_sector(sector,addr):
	sector_addr = sector*1024 + 0x08000000
	#print sector_addr
	addr_hex = int(addr,16)
	#print format(sector_addr, '#04x'), format(addr_hex, '#04x')
	if (addr_hex > sector_addr and addr_hex < (sector_addr+0x400)):
		return True
	else:
		return False
						
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

					
#	for s in symbols:
#		print s.address, s.size, s.file, s.name
					
				
    		
 	
#===============================
# Print memory mapping in the console
#
sector=20
current_address=0x00
symbol_Idx=0
current_address = int(symbols[0].address,16)

print "_________________________________________________"
#for s in symbols:
while ( current_address < 0x0800ffff):
	while (addr_in_sector(sector,symbols[symbol_Idx].address) == True) :
		#if ( addr_in_sector(sector,symbols[symbol_Idx].address) == True):
		addr = int(symbols[symbol_Idx].address,16)
		#print format(current_address, '#04x'), format(addr, '#04x')
		if ( current_address == addr):
			print format(current_address, '#04x'), "|\t", symbols[symbol_Idx].name
		else:
			print format(current_address, '#04x'), "|\t\t\t\t|"

		current_address+=4

		if ( current_address >= ( int(symbols[symbol_Idx].address,0)+int(symbols[symbol_Idx].size,0) ) ):
			symbol_Idx = symbol_Idx+1
			#print symbol_Idx
			#print format(current_address, '#04x')
		
		
				
	current_address+=4
	current_address+=int(symbols[symbol_Idx].size,0)
	symbol_Idx = symbol_Idx+1
	#print symbol_Idx
'''
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
