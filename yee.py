#https://yeelight.readthedocs.io/en/stable/ for yeelight documentation
#needs PIL and yeelight installed
import time
from PIL import ImageGrab
from colorsys import rgb_to_hsv
import yeelight

time.sleep(1)
#ip.txt-ből kiolvassa az ip-ket, vagy automata scan, vagy kézi megadás
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
	bulbs.append(yeelight.Bulb("192.168.1." + line.strip(), effect="smooth", duration=2000))
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
while True:
	#TODO: n izzó esetén (list)
	image = ImageGrab.grab()
	coords[0] = image.getpixel((400, 350)) 	# pixel bal felső sarokból mérve (horizontális, vertikális) koordináták 
	coords[1] = image.getpixel((768, 350))	# (pl. 1366x768: jobb alsó sarok (1365, 767))
	coords[2] = image.getpixel((1000, 350))
	for i in range(len(coords)):
		r_coord = coords[i][0]
		g_coord = coords[i][1]
		b_coord = coords[i][2]
		unadj_hsv = rgb_to_hsv(r_coord, g_coord, b_coord)
		coords[i] = (unadj_hsv[0]*360, max(1,unadj_hsv[1]*100), max(1,unadj_hsv[2]))
		print(coords[i])
	bulbs[0].set_hsv(coords[0][0], coords[0][1], coords[0][2])
	bulbs[1].set_hsv(coords[1][0], coords[1][1], coords[1][2])
	bulbs[2].set_hsv(coords[2][0], coords[2][1], coords[2][2])
	time.sleep(2)


"""
	#image.show()
	for y in range(0, 100, 10):
		for x in range(0, 100, 10):
			color = image.getpixel((x, y))
			#print(color)
"""