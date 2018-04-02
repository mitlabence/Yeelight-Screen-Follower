#https://yeelight.readthedocs.io/en/stable/ for yeelight documentation
#needs PIL and yeelight installed
import time
from PIL import ImageGrab
from colorsys import rgb_to_hsv
import yeelight

time.sleep(1)
value_manually_set = False
value = int(input("adj meg egy value értéket (0 ha automatikus)\n"))
x1 = 800
y1 = 400
x2 = 1000 #1700
y2 = 400
x3 = 300
y3 = 600 #800

if value != 0:
	value_manually_set = True
#ip.txt-ből kiolvassa az ip-ket, vagy automata scan, vagy kézi megadás
if input("Ki akarod választani a pixeleket?\ny/n\n") == "y":
	print("Formátum: szélesség magasság, szóközökkel elválasztva, pl. 1366 768")
	x1, y1 = list(map(int, input("Első pixel: ").split()))
	x2, y2 = list(map(int, input("Első pixel: ").split()))
	x3, y3 = list(map(int, input("Első pixel: ").split()))

try:
	f = open("ip.txt", "r") #file: n sor, az ip utolsó része minden sorban
	print("ip.txt megtalálva")
	
except FileNotFoundError:
	inp = input("ip file nem található, megpróbáljam megtalálni az égők ip címét?\ny/n\n")
	if (inp != "y") & (inp != "n"):
		while (inp != "y") and (inp != "n"):
			inp = input("kérlek válassz y/n közül, y = megkeressem az ip-ket, n = manuális megadás\n")
	if inp == "y":
		print("scannelés megkezdve, ha nem történik semmi pár másodpercen belül, sajnos nem működik")
		bulbs_data = yeelight.discover_bulbs()
		f = open("ip.txt", "w+")
		for bulb in bulbs_data:
			ip = bulb['ip']
			print("égő megtalálva: " + ip)
			f.write(ip.split(".")[-1] + "\n")
		f.close()
	elif inp == "n":
		print("manuális ip megadás")
		#TODO: n izzó
		f = open("ip.txt", "w+")
		inp = input("add meg az első izzó ip-jét\n192.168.1.")
		f.write(inp + "\n")
		inp = input("add meg a második izzó ip-jét\n192.168.1.")
		f.write(inp + "\n")
		inp = input("add meg a harmadik izzó ip-jét\n192.168.1.")
		f.write(inp + "\n")
		f.close()

		
bulbs = list()	
f = open("ip.txt", "r")
for line in f:	#strip(): eltűnteti a \n-eket
	bulbs.append(yeelight.Bulb("192.168.1." + line.strip(), effect="smooth", duration=1100))
"""	
teszt
for i in range(len(bulbs)):
	bulbs[i].turn_off()
while True:
	for bulb in range(len(bulbs)):
		bulbs[bulb].turn_on(effect="smooth", duration=2)
		time.sleep(2)
	for bulb in range(len(bulbs)):
	    bulbs[bulb].turn_off(effect="smooth", duration=2)
	    time.sleep(2)
"""
for i in range(len(bulbs)):
	bulbs[i].turn_on()
coords = [tuple(), tuple(), tuple()]
turned_off = [False, False, False]
while True:
	#TODO: n izzó esetén (list)
	image = ImageGrab.grab()
	coords[0] = image.getpixel((x1, y1)) 	# pixel bal felső sarokból mérve (horizontális, vertikális) koordináták 
	coords[1] = image.getpixel((x2, y2))	# (pl. 1366x768: jobb alsó sarok (1365, 767))
	coords[2] = image.getpixel((x3, y3))
	for i in range(len(coords)):
		r_coord = coords[i][0]
		g_coord = coords[i][1]
		b_coord = coords[i][2]
		if (r_coord == 0 and g_coord == 0 and b_coord == 0):
			bulbs[i].turn_off()
			turned_off[i] = True
			continue
		else:
			if turned_off[i]:
				bulbs[i].turn_on(effect="smooth", duration = 1100)
				turned_off[i] = False
		unadj_hsv = rgb_to_hsv(r_coord, g_coord, b_coord)
		if not(value_manually_set):
			value = max(1, unadj_hsv[2])
		coords[i] = (unadj_hsv[0]*360, max(1,int(unadj_hsv[1]*100)), value)			
		
	bulbs[0].set_hsv(coords[0][0], coords[0][1], coords[0][2])
	bulbs[1].set_hsv(coords[1][0], coords[1][1], coords[1][2])
	bulbs[2].set_hsv(coords[2][0], coords[2][1], coords[2][2])
	time.sleep(1.1)


"""
	#image.show()
	for y in range(0, 100, 10):
		for x in range(0, 100, 10):
			color = image.getpixel((x, y))
			#print(color)
"""
