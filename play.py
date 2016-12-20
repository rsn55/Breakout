# play.py
# Rachel Nash (rsn55) and Jessie Liu (jl2686)
# November 23, 2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    It has methods to update/move the ball and move paddle.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Bricks]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left
    
        _status [string 'oops', or None if ball in play]: whether or not ball went off screen
        _storebrick [stores how many bricks there are at beginning]
        _level [int, either 1 or 2]: level of the game
        _ball2 [Ball, or None if in Level 1 or waiting for serve]: second ball to animate
        
    """
    
    def getLevel(self):
        return self._level
    def getStoredBricks(self):
        return self._storebrick
    def getStatus(self):
        return self._status
    def setStatus(self,new):
        self._status = new
    def getTries(self):
        return self._tries
    def getBrickLength(self):
        return len(self._bricks)
    
    def __init__(self, level):
        """Initializer to create paddles and bricks.
        
        Parameter: level
        Precondition: Must be an int (either 1 or 2)."""
        bricklist = []
        row = 1
        column = 1
        while (column <= BRICKS_IN_ROW+1) and (row <= BRICK_ROWS):
            if column == BRICKS_IN_ROW+1:
                column = 1
                row = row + 1
            else:
                remainder = row%10
                curlinecolor = BRICK_COLORS[remainder-1]
                curfillcolor = curlinecolor
                curleft = BRICK_SEP_H/2.0 + BRICK_WIDTH*(column-1) + BRICK_SEP_H*(column-1)
                curtop = GAME_HEIGHT-BRICK_Y_OFFSET - BRICK_HEIGHT*(row-1) - BRICK_SEP_V*(row-1)
                newbrick = Brick(curtop,curleft,curlinecolor,curfillcolor)
                column = column + 1
                bricklist.append(newbrick)
        self._bricks = bricklist
        self._paddle = Paddle(GAME_WIDTH/2.0)
        self._ball = None
        self._ball2 = None
        self._tries = 3
        self._status = None
        self._storebrick = len(bricklist)
        self._level = level
    
    def updatePaddle(self,input):
        """Helper method called by Breakout to update position
        of the paddle when left and right arrow keys are pressed.
        Moves the paddle -12 if left key is pressed and +12 if
        right key is pressed. Prevents paddle from going offscreen.
        
        Parameter: input
        Precondition: must be keyboard input from Breakout
        
        **Citation: Understanding of inputs and movement taken from
        lecture code 'arrows.py' by Walter White, finished
        November 17, 2014."""

        start_pos = self._paddle.getX()
        da = 0
        if input.is_key_down('left'):
            da -= 12
        if input.is_key_down('right'):
            da += 12
        if (start_pos + da) > (GAME_WIDTH-PADDLE_WIDTH/2.0):
            self._paddle.setX(GAME_WIDTH-PADDLE_WIDTH/2.0)
        elif (start_pos + da) < (PADDLE_WIDTH/2.0):
            self._paddle.setX(PADDLE_WIDTH/2.0)
        else:
            self._paddle.setX(start_pos + da)
        
    def updateBall(self):
        """Method to update the position of the ball.
        Different actions are taken if there are 2 balls
        or only 1 ball (determined by level 1 or level 2).
        Checks if ball goes offscreen."""
        self._updateSingleBall(self._ball)
        if self._ball2 is not None:
            self._updateSingleBall(self._ball2)
        self._checkLostBall()    
    
    def _updateSingleBall(self,ball):
        """Helper method to update a ball. Ball bounces off of top, left,
        and right of screen. Bounce means the vertical velocity is negated.
        If ball bounces off of bricks, the brick is removed from the list and
        disappears from the screen.
        If Level 1, the ball moves by adding the current velocity onto the x
        and y positions.
        If Level 2, the balls move slightly slower by adding a the fraction
        of the current velocity onto the x and y positions.
        If one of the balls goes offscreen in Level 2, the other ball
        increases in speed (the same speed as Level 1).
        
        Parameter: ball
        Precondition: must be type Ball() from Models.py"""
        if (ball.getRight() >= GAME_WIDTH) or (ball.getLeft() <= 0):
            ball.setxvel(-ball.getxvel())
        elif (ball.getTop() >= GAME_HEIGHT):
            ball.setyvel(-ball.getyvel())
        if self._paddle.collides(ball):
            ball.setyvel(-ball.getyvel())
        for x in self._bricks:
            if x.brickCollides(ball):
                ball.setyvel(-ball.getyvel())
                self._bricks.remove(x)
        if self._level == 1:
            ball.setX(ball.getX() + ball.getxvel())
            ball.setY(ball.getY() + ball.getyvel())
        elif self._level == 2:
            if ball == self._ball:
                if ball.getCheck() == 'no':
                    ball.setX(ball.getX() + ball.getxvel()/1.25)
                    ball.setY(ball.getY() + ball.getyvel()/1.25)
                else:
                    ball.setX(ball.getX() + ball.getxvel())
                    ball.setY(ball.getY() + ball.getyvel())
            if ball == self._ball2:
                if ball.getCheck() == 'no':      
                    ball.setX(ball.getX() + ball.getxvel()/2)
                    ball.setY(ball.getY() + ball.getyvel()/2)
                else:
                    ball.setX(ball.getX() + ball.getxvel())
                    ball.setY(ball.getY() + ball.getyvel())
            
    def _checkLostBall(self):
        """Helper method to check if ball has gone offscreen.
        In level 1, one ball going off results in losing a try.
        In level 2, both balls must go offscreen to lose a try."""
        if (self._ball.getTop() <=0) and self._level == 1:
            self._tries -= 1
            self._status = 'oops'
        if self._level == 2:
            if (self._ball.getTop() <=0) or (self._ball2.getTop()<=0):
                self._ball.setCheck('yes')
                self._ball2.setCheck('yes')
            if (self._ball.getTop() <=0) and (self._ball2.getTop() <=0):
                self._tries -= 1
                self._status = 'oops'         
        
    def serveBall(self):
        """'Serves' or creates a new ball. 1 ball is served if
        in Level 1, but 2 are served in Level 2."""
        if self._level < 2:
            self._ball = Ball()
        if self._level == 2:
            self._ball = Ball()
            self._ball2 = Ball()
        
    def draw(self, view):
        """Draw method to draw bricks, paddle, balls."""
        for x in self._bricks:
            x.draw(view)
        self._paddle.draw(view)
        if self._ball is not None:
            self._ball.draw(view)
        if self._ball2 is not None:
            self._ball2.draw(view)
