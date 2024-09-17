import pygame, math, time, threading, random

#spinner colors/names
options = [(202, 242, 138), (127, 221, 240),
	(127, 136, 240), (159, 71, 181),
	(219, 92, 219), (219, 92, 109)]
names = ["Green", "Blue", "Indigo", "Violet", "Magenta", "Red"]

#data
size = 450
radius = (size*(3/5))/2
margin = 12
start = time.time()
spinning = False

#design functions
def background(screen, size):
	pygame.draw.rect(screen, (230, 115, 0), [size/3-5, 0, 10, size/2])
	pygame.draw.rect(screen, (230, 115, 0), [size*(2/3)-5, 0, 10, size/2])
	pygame.draw.circle(screen, (25, 25, 25), [size/2, size/2], (size*(3/5))/2)

def board(screen, radius, pos, colors, margin):
	step = 360/len(colors)
	
	for clr in range(len(colors)):
		angle = step*(clr+1)-step/2

		new_pos = [pos[0] + math.cos(angle*((2*math.pi)/360))*margin/2,
			pos[1] - math.sin(angle*((2*math.pi)/360))*margin/2]

		corner = [new_pos[0] - (radius-margin),
			new_pos[1] - (radius-margin)]
		
		pygame.draw.arc(screen, colors[clr], [corner, [(radius-margin)*2]*2],
			(angle-step/2)*((2*math.pi)/360), (angle+step/2)*((2*math.pi)/360),
			int(radius-margin))


#functionality functions (*bu-dum tsh*)
def determine():
	global arrow_angle, options, names, landed, landed_rect, display, size
	step = 360/len(options)
	determined = False
	
	for opt in range(len(options)):
		if determined:
			continue
		
		max = step*(opt+1)
		min = step*opt

		if arrow_angle >= min and arrow_angle < max:
			landed = font.render(names[opt], True, options[opt])
			landed_rect = landed.get_rect()
			landed_rect.center = (size/2, size*(3/20))

			pygame.draw.rect(display, (50, 50, 50), [size/3+5, landed_rect.top, size/3-10, landed_rect.height])
			display.blit(landed, landed_rect)

			pygame.draw.rect(display, (230, 115, 0), [size*(2/3)-5, landed_rect.top, 10, landed_rect.height])
			pygame.draw.rect(display, (230, 115, 0), [size/3-5, landed_rect.top, 10, landed_rect.height])
			
			pygame.display.update()
			determined = True

def spin():
	global spinning, spin_thread, arrow, arrow_rect, arrow_angle, display, margin, point2, radius
	iters = 0
	
	of = random.randint(360, 720)
	Vi = math.sqrt(2*of)
	cf = Vi
	
	while cf > 0:
		iters += 1
		cf -= iters/15
		arrow_angle += cf

		if arrow_angle >= 360:
			arrow_angle -= 360
		
		point2 = [size/2+math.cos(math.radians(arrow_angle))*radius*(4/5),
			size/2-math.sin(math.radians(arrow_angle))*radius*(4/5)]

		#update
		pygame.draw.circle(display, (25, 25, 25), [size/2, size/2], (size*(3/5))/2)
		board(display, radius, [size/2]*2, options, margin)
		pygame.draw.line(display, (0, 0, 0), point1, point2, margin)
		
		pygame.display.update()
		time.sleep(1/15)

	determine()
	time.sleep(1)
	
	#reset
	spinning = False
	spin_thread = threading.Thread(target=spin)

#thread
spin_thread = threading.Thread(target=spin)

#initialize
display = pygame.display.set_mode([size, size])
pygame.init()
pygame.font.init()

#texts
font = pygame.font.SysFont("freesanbold", 24)

#click instructions
instruct = font.render("Left click to spin.", True, (200, 200, 200))
instruct_rect = instruct.get_rect()
instruct_rect.center = (size/2, size*(1/20))

#spin output
landed = font.render("", True, (200, 200, 200))
landed_rect = landed.get_rect()
landed_rect.center = (size/2, size*(3/20))

#arrow
arrow_angle = 0

point1 = [size/2]*2
point2 = [size/2 + radius*(4/5), size/2]

#display
display.fill((50, 50, 50))
background(display, size)
board(display, radius, [size/2]*2, options, margin)

display.blit(instruct, instruct_rect)
display.blit(landed, landed_rect)
pygame.draw.line(display, (0, 0, 0), point1, point2, margin)

while True:
	pygame.event.pump()
	events = pygame.event.get()
	
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if not spinning:
				spinning = True
				spin_thread.start()

	pygame.display.update()

