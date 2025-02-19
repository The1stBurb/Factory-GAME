import pygame 
import random
#re color an image
def colorize(image, new_color):
    tinted = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    tinted.fill(new_color)
    tinted.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted
def recolour(image, new_color):
    # Create a copy of the original image
    recolored = image.copy()
    
    # Get the dimensions of the image
    width, height = image.get_size()
    
    # Lock the surface for pixel manipulation
    recolored.lock()
    
    # Iterate through each pixel
    for x in range(width):
        for y in range(height):
            # Get the current pixel color
            current_color = image.get_at((x, y))
            
            # Calculate the intensity (assuming R, G, and B are equal in greyscale)
            intensity = current_color.r / 255.0
            
            # Calculate the new color components
            new_r = int(new_color[0] * (1 - intensity))
            new_g = int(new_color[1] * (1 - intensity))
            new_b = int(new_color[2] * (1 - intensity))
            
            # Set the new color
            recolored.set_at((x, y), (new_r, new_g, new_b, current_color.a))
    
    # Unlock the surface
    recolored.unlock()
    
    return recolored
#resize an image
def resize(img,w,h):
    return pygame.transform.scale(img,(w,h))
#rotate an image
def rot90(img,r):
    # if r==-1:
    #     r=random.randint(0,3)*90
    return pygame.transform.rotate(img,r*90)
def rotate_image(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
#create a rectanngle
def rect(screen,x,y,w,h,col=(255,255,255),width=0):
    # print(col)
    pygame.draw.rect(screen, col, pygame.Rect(x, y, w, h),width)
#write text
def text(screen,font,txt,x,y,col=(0,0,0)):
    screen.blit(font.render(txt, True, col),(x,y))
#make a quadrilateral
def quad(screen,x1,y1,x2,y2,x3,y3,x4,y4,col=(255,255,255)):
    pygame.draw.polygon(screen, col, [(x1,y1),(x2,y2),(x3,y3),(x4,y4),])
#blit an image
def image(screen,img,x,y):
    screen.blit(img,(x,y))
#pull image form path
def gitImg(path):
    return pygame.image.load(path).convert_alpha()
#pull image and resize lol
def imgGit(path,w,h):
    return resize(gitImg(path),w,h)