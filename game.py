import pygame

pygame.init()
screen_width=1200
screen_height=700
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("asdf")

class Bike:
	"""This is to store the different moving pieces of the bike. The body is the whole thing, while the front and the back wheels move. All the wheels are relative to the body of the bike"""
	def __init__(self, body_x, body_y, front_wheel_x,front_wheel_y, back_wheel_x,back_wheel_y):
		self.body_x=body_x
		self.body_y=body_y
		self.front_wheel_y=front_wheel_x
		self.front_wheel_x=front_wheel_y
		self.back_wheel_x=back_wheel_x
		self.back_wheel_y=back_wheel_y
	def tire_position_update(self):
		self.back_wheel_x=self.body_x+38 #loading front wheel
		self.back_wheel_y=self.body_y+105
		self.front_wheel_x=self.body_x+111 #loading back wheel
		self.front_wheel_y=self.body_y+40

#initiatlizing
bike=Bike(10, 450,1,1,1,1) #where the pieces first load I have always been driven by the prospects of taking on new challenges
width= 80
height= 40
velocity=0
rect_colour= (255,0,0)
left=False
right=True
walkCount=0
clock=pygame.time.Clock()
isJump=False
jumpcount=7
acceleration= 2
decceleration=2
braking=2


#images loading
moveleft=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35), pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35)]
#moveright=[pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False),pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False)] **no need for this anymore as you can't move left
backwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(45,45)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(45,45))]
frontwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(45,45)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(45,45))]
background= pygame.image.load('bg.png')

#wheels temporary position/testing ***not working!!
win.blit(frontwheel_img[1],(bike.front_wheel_x,bike.front_wheel_y))
win.blit(backwheel_img[0],(bike.back_wheel_x,bike.back_wheel_y))

#functions
def redrawgamewindow():
	global walkCount #for having an animation when moving

	win.blit(background, (0,0))
	if walkCount >1:
		walkCount= 0

	if left:
		win.blit(moveleft[walkCount],(bike.body_x,bike.body_y))
		walkCount+=1

	elif right:
		win.blit(moveleft[walkCount],(bike.body_x,bike.body_y))
		walkCount+=1


	bike.tire_position_update()
	win.blit(frontwheel_img[1],(bike.front_wheel_x,bike.front_wheel_y))
	win.blit(backwheel_img[0],(bike.back_wheel_x,bike.back_wheel_y))


	pygame.display.update()

#main loop to run the game
while(True):
	redrawgamewindow()
	clock.tick(60)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()

	keys= pygame.key.get_pressed()
	if keys[pygame.K_w] and bike.body_x<=(screen_width-width):
		velocity+=acceleration
		#bike.body_x+=velocity
		#right=True
		#left=False

	elif keys[pygame.K_s] and bike.body_x>=0:
		velocity-=braking
		#bike.body_x-=velocity
		#left=True
		#right=False

	elif(velocity<0 and bike.body_x<=(screen_width-width)):
		velocity+=2

	elif(velocity>0 and bike.body_x<=(screen_width-width)):
		velocity-=2

	#jumping
	if not(isJump):
		if keys[pygame.K_SPACE]:
			isJump= True
	else:
		if jumpcount >= -7:
			neg= 1
			if jumpcount<0:
				neg=-1
			bike.body_y-= (jumpcount**2)*0.5*neg
			jumpcount-=1

		else:
			isJump=False
			jumpcount=7

	bike.body_x+=velocity #main movingscreen_width-width
