# models.py
# Rachel Nash (rsn55) and Jessie Liu (jl2686)
# November 23, 2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.
    
    The attributes of this class are those inherited from GRectangle.
    """
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,new):
        self.x = new
    
    def __init__(self,xpoint):
        """Initializer to create a new Paddle"""
        color = colormodel.BLACK
        GRectangle.__init__(self,x=xpoint,y=PADDLE_OFFSET+PADDLE_HEIGHT/2.0,linecolor=color,
                            fillcolor=color, width=PADDLE_WIDTH,height=PADDLE_HEIGHT)
  
    def collides(self,ball):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        r = ball.getWidth()/2.0
        x = ball.getX()
        y = ball.getY()
        tl = [x-r,y+r]
        tr = [x+r,y+r]
        bl = [x-r,y-r]
        br = [x+r,y-r]
        list = [tl,tr,bl,br]
        if ball.getyvel() <0:
            for c in list:
                if self.contains(c[0],c[1]):
                    return True
                else:
                    return False
        else:
            return False


class Brick(GRectangle):
    """An instance is a single brick.
    
    This class contains a method to detect collision with the ball.
    
    The attributes of this class are those inherited from GRectangle.
    
    Attribute:
    _collision_status: True if there has been a collision, False otherwise
    """
    
    def getCollisionStatus(self):
        return self._collision_status

    def __init__(self,top,left,alinecolor,afillcolor):
        """Initializer to create a new Brick.
        
        Parameter: top
        Precondition: int or float 
        
        Parameter: left
        Precondition: int or float
        
        Parameter: alinecolor
        Precondition: must be a color from colormodel and the same
            as 'afillcolor'
        
        Parameter: afillcolor
        Precondition: must be a color from colormodel and the same
            as 'alinecolor'"""
        assert alinecolor == afillcolor
        xpoint = left+BRICK_WIDTH/2.0
        ypoint = top-BRICK_HEIGHT/2.0
        GRectangle.__init__(self,x=xpoint,y=ypoint,linecolor=alinecolor,fillcolor=afillcolor,
                            width=BRICK_WIDTH,height=BRICK_HEIGHT)
        self._collision_status = False
    
    def brickCollides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        r = ball.getWidth()/2.0
        x = ball.getX()
        y = ball.getY()
        tl = [x-r,y+r]
        tr = [x+r,y+r]
        bl = [x-r,y-r]
        br = [x+r,y-r]
        list = [tl,tr,bl,br]
        for c in list:
            if self.contains(c[0],c[1]):
                return True
            else:
                return False


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction
   
        _checkOther [string, either 'yes' or 'no']:
                used in Level 2 when there are two balls. If one of the balls goes
                offscreen, but the other remains, they are turned to 'yes'.
                Initially set to 'no'.
    """
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,new):
        self.x = new
    def setY(self,new):
        self.y = new
        
    def getTop(self):
        return self.top
    def getBottom(self):
        return self.bottom
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    
    def getxvel(self):
        return self._vx
    def getyvel(self):
        return self._vy
    def setxvel(self,new):
        self._vx = new
    def setyvel(self,new):
        self._vy = new
        
    def getCheck(self):
        return self._checkOther
    def setCheck(self,new):
        self._checkOther = new
        
    def getWidth(self):
        return self.width

    def __init__(self):
        """Initializer to set random velocity."""
        color = colormodel.BLACK
        GEllipse.__init__(self,x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=BALL_DIAMETER,
                          height=BALL_DIAMETER,fillcolor=color,linecolor=color)
       
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
        self._checkOther = 'no'
    
