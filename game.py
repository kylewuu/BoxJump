import pygame
import time
import random

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
bike=Bike(12, 200,1,1,1,1) #where the pieces first load
tile_x=150
tile_y=540
tileYMark=540
tire_diameter=45
width= 80
height= 40
velocity=0
rect_colour= (255,0,0)
left=False
right=True
walkCount=0
clock=pygame.time.Clock()
isJump=False
jumpcount=10
acceleration= 5
decceleration=5
backacceleration=0.5
max_velocity=15
no_forward= False
no_backward= False #for collisions on side of crates
quadrant=1
tile_length=60
gravity=1
bike.tire_position_update()
default_land=600
temp_land=tile_y
#for the new jumping system
gravity=10
y_velocity=0
initial_y_velocity=60

#images loading
moveleft=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35), pygame.transform.rotate(pygame.transform.scale(pygame.image.load('offroad/body.png'),(140,80)),35)]
#moveright=[pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False),pygame.transform.flip(pygame.transform.scale(pygame.image.load('offroad/body.png'),(300,180)), True, False)] **no need for this anymore as you can't move left
backwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(tire_diameter,tire_diameter)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(tire_diameter,tire_diameter))]
frontwheel_img=[pygame.transform.scale(pygame.image.load('offroad/tire.png'),(tire_diameter,tire_diameter)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load('offroad/tire.png'),(90)),(tire_diameter,tire_diameter))]
background= pygame.image.load('bg.png')

#tiles
tiles=pygame.transform.scale(pygame.image.load('tiles/Crate.png'), (tile_length,tile_length))
tiles_array=[]
#initial tile generating
tilesArrayX=[50,200,350,500,650,800,950,1100]
tilesArrayY=[0,0,0,0,0,0,0,0]
tileSizes=[1,2,3]

#initializing tile heights
for i in range(8):
	tilesArrayY[i]=random.choice(tileSizes)

#functions
def tilesGeneration():
	for i in range(8):
		if(tilesArrayY[i]==1):
			win.blit(tiles,(tilesArrayX[i], tileYMark))

		elif(tilesArrayY[i]==2):
			win.blit(tiles,(tilesArrayX[i], tileYMark))
			win.blit(tiles,(tilesArrayX[i], tileYMark-tile_length))

		elif(tilesArrayY[i]==3):
			win.blit(tiles,(tilesArrayX[i], tileYMark))
			win.blit(tiles,(tilesArrayX[i], tileYMark-tile_length))
			win.blit(tiles,(tilesArrayX[i], tileYMark-(tile_length*2)))

def tileDetection():
	global tile_x
	global tile_y
	closest=500
	tempDistance=0
	for i in range(8):
		tempDistance=abs(tilesArrayX[i]-bike.back_wheel_x)
		if (tempDistance<closest):
			closest=tempDistance
			closestIndex=i
	tile_x=tilesArrayX[closestIndex]
	tile_y=tileYMark-(tile_length*(tilesArrayY[closestIndex]-1))

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

	#tiles drawing
	tilesGeneration()
	tileDetection()
	pygame.display.update()

def gravityCheck(tempLandTemp, yVelocityTemp,tire_bottom_collide):
	numFall=int(yVelocityTemp/10)
	if (numFall<0):
		numFall=numFall*(-1)
		for p in range(numFall):
			bike.tire_position_update()
			tire_bottom_collide=bike.back_wheel_y+tire_diameter

			if(tire_bottom_collide<tempLandTemp):
				bike.body_y+=10

	elif (numFall>0):
		for n in range(numFall):
			bike.tire_position_update()
			tire_bottom_collide=bike.back_wheel_y+tire_diameter

			if(tire_bottom_collide<=tempLandTemp):
				bike.body_y-=10

#main loop to run the game
while(True):

	redrawgamewindow()
	clock.tick(60)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()

	keys= pygame.key.get_pressed()

	#collision walls
	tire_left_collide=bike.back_wheel_x
	tire_right_collide=bike.back_wheel_x+tire_diameter
	tire_bottom_collide=bike.back_wheel_y+tire_diameter


	#quadrant testings
	if (tire_right_collide<=tile_x and bike.back_wheel_y>tile_y):
		quadrant=1

	elif(tire_right_collide<=tile_x and bike.back_wheel_y<tile_y):
		quadrant=2

	elif(bike.back_wheel_x<tile_x+tile_length and tire_right_collide>tile_x and tire_bottom_collide<tile_y):
		quadrant=3

	elif(tire_bottom_collide<=tile_y and bike.back_wheel_x>=tile_x+tile_length):
		quadrant=4

	elif(tire_bottom_collide>tile_y and bike.back_wheel_x>=tile_x+tile_length):
		quadrant=5

	if quadrant==1:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity and no_forward==False and tire_right_collide<tile_x:
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity:
			bike.body_x-=decceleration

		elif tire_right_collide>=tile_x:
			no_forward=True

		elif tire_right_collide<tile_x:
			no_forward=False

		temp_land=default_land

		#new jumping (not too sure if it'll work)
		if(tire_bottom_collide<temp_land and y_velocity>=-50):
			y_velocity-=gravity

		elif (tire_bottom_collide>=temp_land):
			y_velocity=0
			isJump=False
			if not(isJump):
				if keys[pygame.K_SPACE]:
					isJump= True
					y_velocity=initial_y_velocity


		gravityCheck(temp_land,y_velocity, tire_bottom_collide)

		# bike.body_y-=y_velocity


	elif (quadrant==2):
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity:
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity:
			bike.body_x-=decceleration

		temp_land=default_land

		#new jumping (not too sure if it'll work)
		if(tire_bottom_collide<temp_land and y_velocity>=-50):
			y_velocity-=gravity

		elif (tire_bottom_collide>=temp_land):
			y_velocity=0
			isJump=False
			if not(isJump):
				if keys[pygame.K_SPACE]:
					isJump= True
					y_velocity=initial_y_velocity

		gravityCheck(temp_land,y_velocity, tire_bottom_collide)
		# bike.body_y-=y_velocity


	elif quadrant==3:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity and tire_bottom_collide<=tile_y:
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity:
			bike.body_x-=decceleration

		temp_land=tile_y

		#new jumping
		if(tire_bottom_collide<temp_land and y_velocity>=-50):
			y_velocity-=gravity

		elif (tire_bottom_collide>=temp_land):
			y_velocity=0
			isJump=False
			if not(isJump):
				if keys[pygame.K_SPACE]:
					isJump= True
					y_velocity=initial_y_velocity

		gravityCheck(temp_land,y_velocity,tire_bottom_collide)


	elif quadrant==4:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity:
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity:
			bike.body_x-=decceleration

		temp_land=default_land

		#new jumping (not too sure if it'll work)
		if(tire_bottom_collide<temp_land and y_velocity>=-50):
			y_velocity-=gravity

		elif (tire_bottom_collide>=temp_land):
			y_velocity=0
			isJump=False
			if not(isJump):
				if keys[pygame.K_SPACE]:
					isJump= True
					y_velocity=initial_y_velocity

		gravityCheck(temp_land,y_velocity, tire_bottom_collide)
		# bike.body_y-=y_velocity


	elif quadrant==5:
		if keys[pygame.K_w] and bike.body_x<=(screen_width-width) and velocity<=max_velocity :
			bike.body_x+=acceleration

		elif keys[pygame.K_s] and bike.body_x>=0 and velocity<=max_velocity and no_backward==False and tire_left_collide>tile_x+tile_length:
			bike.body_x-=decceleration

		elif tire_left_collide<=tile_x:
			no_backward=True

		elif tire_left_collide>tile_x:
			no_backward=False

		temp_land=default_land

		#new jumping (not too sure if it'll work)
		if(tire_bottom_collide<temp_land and y_velocity>=-50):
			y_velocity-=gravity

		elif (tire_bottom_collide>=temp_land):
			y_velocity=0
			isJump=False
			if not(isJump):
				if keys[pygame.K_SPACE]:
					isJump= True
					y_velocity=initial_y_velocity

		gravityCheck(temp_land,y_velocity, tire_bottom_collide)
		# bike.body_y-=y_velocity

	if(tire_bottom_collide==default_land):
		pygame.quit()


	print("q",quadrant, "temp land",temp_land, "tire_bottom_collide",tire_bottom_collide, "y velocity", y_velocity)
