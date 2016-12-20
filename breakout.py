# breakout.py
# Rachel Nash (rsn55) and Jessie Liu (jl2686)
# November 23, 2016
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Any initialization should be done in the start method.
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
        Attribute _gamenum is less than or equal to 5
        Attribute _done is only not None if _state is STATE_COMPLETE and _gamenum==5
        Attribute _scoredict is empty if _gamenum = 0
        Attribute _score is only None if _state is STATE_INACTIVE, STATE_COUNTDOWN,
            STATE_LEVEL2, or STATE_NEWGAME
        Attribute _timer is only 0 if it is the first countdown of the round
        Attribute _scoreboard has GLabels of text='' if _gamenum = 0
    
    _last_keys  [GPoint, None if mouse not down last frame]:
                   last position clicked
    _timer      [int]
                keeps track of how many animation frames pass after
                game enters STATE_COUNTDOWN
    _score      [int, or None if STATE_INACTIVE or STATE_NEWGAME]
                keeps track of how many bricks have been hit in one game
    _scoredict  [dictionary; starts off empty, max length of 5]
                each key is an int and the turn/try number
                each value is a string and the score associated with a particular turn
    _scoreboard [list of GLabels]
                contains labels for each try and score to display in a scoreboard
    _done       [GLabel, or None if not on last try]
                after 5 tries, this message is displayed to indicate
                that the user should close the window
    _gamenum    [int;<=5]
                keeps track of how many games have been played so far    
    _levelinput [int, either 1 or 2]
                keeps track of the level that needs to be inputed into Play
                either Level 1 or Level 2
    """

    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        self._last_keys = 0
        self._game = None
        self._timer = 0
        self._score = None
        self._scoredict = {}
        self._gamenum = 0
        self._done = None
        self._scoreboard = [GLabel(text='',left=50,y=GAME_HEIGHT/2-120,
                                   linecolor = colormodel.RED, font_name='arcade'),
                            GLabel(text='',left=50,y=GAME_HEIGHT/2 - 150,
                                   linecolor = colormodel.ORANGE,font_name='arcade'),
                            GLabel(text='',left=50,y=GAME_HEIGHT/2 - 180,
                                   linecolor = colormodel.RGB(255,241,0),font_name='arcade'),
                            GLabel(text='',left=50,y=GAME_HEIGHT/2 - 210,
                                   linecolor = colormodel.GREEN,font_name='arcade'),
                            GLabel(text='',left=50,y=GAME_HEIGHT/2 - 240,
                                   linecolor = colormodel.CYAN, font_name='arcade')]
        self._state = STATE_INACTIVE
        self._mssg = GLabel(text=str('Welcome to Breakout!\n'
                            'Press any key to play Level 1'),
                            x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                            font_name='arcade')
        self._levelinput = 1
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        The primary purpose of this game is to determine the current state, and
        -- if the game is active -- pass the input to the Play object _game to play the game.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle().
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_COMPLETE: Shows message and scoreboard after each round of gameplay.
        
        STATE_LEVEL2: Shows message to continue on to Level 2 after 5 rounds of Level 1.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        STATE_COMPLETE: Switches to this state if the state was STATE_ACTIVE in
        the previous frame. The ball was either lost with no tries remaining or
        all the bricks were destroyed.
        
        STATE_LEVEL2: The application switches to this state if the state was
        STATE_COMPLETE in the previous frame, 5 game rounds have been played,
        and a key has been pressed.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        
        **Citation: This organization idea is copied from Walter White's lecture
        code in 'state.py', finished November 17, 2015.
        """

        self._determineState()
        if self._state == STATE_INACTIVE:
            self.start()
        elif self._state == STATE_NEWGAME:
            self._newgame()
        elif self._state == STATE_COUNTDOWN:
            self._countdown()
        elif self._state == STATE_ACTIVE:
            self._active()
        elif self._state == STATE_PAUSED:
            self._paused()
        elif self._state == STATE_COMPLETE:
            self._complete()
        elif self._state == STATE_LEVEL2:
            self._level2()
        elif self._state == STATE_ACTIVE2:
            self._active2()
        elif self._state == STATE_PAUSED2:
            self._paused2()
         
    def draw(self):
        """Draws the game objects to the view.
        Draws _mssg, _score, _game, _scoreboard, _done.
        """
        if self._mssg is not None:
            self._mssg.draw(self.view)
        if (self._score is not None):
            self._score.draw(self.view)
        if self._state not in [STATE_INACTIVE,STATE_COMPLETE, STATE_LEVEL2]:
            self._game.draw(self.view)
        if (self._state is STATE_COMPLETE) and (len(self._scoredict) != 0):
            for x in self._scoreboard:
                x.draw(self.view)
        if self._done is not None:
            self._done.draw(self.view)
        
    def _determineState(self):
        """Helper method for update that changes the state if necessary.
        If state is INACTIVE and a key is pressed, it moves to NEWGAME.
        If state is ACTIVE, ball goes off screen, and there are tries left,
            it moves to PAUSED.
        If state is PAUSED and a key is pressed, it moves to COUNTDOWN.
        If state is ACTIVE, ball goes off screen, and there are no tries
            left, state goes to COMPLETE.
        If state is ACTIVE and all the bricks are eliminated, it moves to
            state COMPLETE.
        If state is COMPLETE, a key is pressed, and the player has not
            yet reached the limit of 5 games, it moves to NEWGAME.
        If state is COMPLETE, a key is pressed, and the player has
             reached the limit of 5 games, it moves to LEVEL2.
        If state is LEVEL2 and a key is pressed, the state moves to NEWGAME.
        ***Citation: Understanding of key count and state change was
        taken from looking at Walter White's lecture
        code in 'state.py', finished November 17, 2015."""
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self._last_keys == 0
        if change and (self._state == STATE_INACTIVE):
            self._state = STATE_NEWGAME
        self._last_keys= curr_keys
        if self._state == STATE_ACTIVE:
            if (self._game.getStatus() == 'oops') and (self._game.getTries() != 0):
                self._state = STATE_PAUSED
                self._game.setStatus(None)
            elif (self._game.getStatus() == 'oops') and (self._game.getTries() == 0):
                self._gamenum += 1
                self._state = STATE_COMPLETE
        elif self._state == STATE_COMPLETE and change:
            self._helpcompletechange()
        elif self._state == STATE_LEVEL2 and change:
            self._state = STATE_NEWGAME
        if self._state == STATE_PAUSED and change:
            self._mssg = None
            self._state = STATE_COUNTDOWN
        if self._state == STATE_ACTIVE and self._game.getBrickLength() == 0:
            self._gamenum += 1
            self._state = STATE_COMPLETE

    def _helpcompletechange(self):
        """Helper method for _determineState. Only called if
        self._state is STATE_COMPLETE and change."""
        if self._gamenum <5:
            self._state = STATE_NEWGAME
        elif self._gamenum == 5:
            if self._levelinput == 1:
                self._state = STATE_LEVEL2
            else:
                self._state = STATE_INACTIVE
    
    def _updateScore(self):
        """Helper method for COUNTDOWN and ACTIVE to display how many
        bricks a player has eliminated. For instance, if 1 brick is
        collided with and disappears, it displays 'SCORE: 1'.
        Nothing is displayed in INACTIVE.
        Score is always 0 in COUNTDOWN."""
        if self._state == STATE_INACTIVE:
            self._score = None
        elif (self._state == STATE_COUNTDOWN):
            self._score = GLabel(text='SCORE: 0',x=GAME_WIDTH/2,y=GAME_HEIGHT-25,
                                 linecolor=colormodel.GRAY, font_name='arcade')
        elif self._score is not None:
            self._score.text = str('SCORE: '+
                            str(self._game.getStoredBricks()-self._game.getBrickLength()))
            
    def _newgame(self):
        """Helper method for operations of _state STATE_NEWGAME.
        Only called when game is in this state.
        Creates GUIs of Play() and displays them on the screen.
        Only lasts one animation frame."""
        self._done = None
        if self._mssg is not None:
            self._mssg.text = ''
        self._game = Play(self._levelinput)
        self._state = STATE_COUNTDOWN
        
    def _countdown(self):
        """Helper method for operations of _state STATE_COUNTDOWN.
        Only called when game is in this state.
        If this is the first countdown of the game round, there are
        GLabels counting 3-2-1 until state is switched.
        If this is not the first countdown, state moves to ACTIVE.
        Timer keeps track of animation frames, which change 60 times
        per second. So after 60 animation frames, 1 second has passed.
        There is a gap between number changes of 3-2-1.
        The paddle can be moved in this state so the players can orient
        themselves, but there is no ball."""
        self._done = None
        if self._mssg is not None:
            self._mssg.text = ''
        self._updateScore()
        self._timer += 1
        self._game.updatePaddle(self.input)
        if 0 <= self._timer < 60-WAIT_TIME:
           self._mssg = GLabel(text='3',x=GAME_WIDTH/2,
                               y=GAME_HEIGHT/2, font_name='arcade')
        if 60-WAIT_TIME <= self._timer < 60+WAIT_TIME:
           self._mssg.text = ''
        if 60+WAIT_TIME <= self._timer < 120-WAIT_TIME:
            self._mssg.text = '2'
        if 120-WAIT_TIME <= self._timer < 120+WAIT_TIME:
            self._mssg.text = ''
        if 120+WAIT_TIME <= self._timer < 180:
            self._mssg.text = '1'
        if self._timer == 180:
            self._mssg = None
        if self._timer > 180:
            self._game.serveBall()
            self._state = STATE_ACTIVE
            
    def _active(self):
        """Helper method when _state is STATE_ACTIVE.
        Only called when in this state.
        Allows the player to move the paddle to hit the ball and
        (hopefully) bounce the ball onto the bricks.
        As each brick is hit, the score is updated to reflect the change."""
        self._done = None
        self._mssg = None
        self._updateScore()
        self._game.updatePaddle(self.input)
        self._game.updateBall()
        
    def _paused(self):
        """Helper method when _state is STATE_PAUSED.
        Only called when in this state.
        Displayed if a player loses a ball but has tries left.
        Displays a message to press a key for a new serve.
        Gets rid of ball (though it will be offscreen anyway)."""
        self._mssg = GLabel(text='Press any key for a new ball',
                            x=GAME_WIDTH/2,y=GAME_HEIGHT/2, font_name='arcade')
        self._ball = None
        self._done = None
        
    def _complete(self):
        """Helper method when _state is STATE_COMPLETE.
        Only called when in this state.
        Ball is reset.
        'SCORE: [score]' is still in view at the top of the screen.
        There are two possibilities:
           1. Winning (see _wincomplete specification)
           2. Losing (see _losecomplete specification)
        If the player has had less than 5 turns, they are told to press
        any key to play again. If they reach 5 turns, a message is displayed
        that says to go on to level 2.
        
        Scoreboard works by adding scores to a dictionary with the key
        being the chronological try # of that game. Dictionary is sorted to
        display the first try first and so on.
        _done is used to display the message after 5 turns
        _mssg is used to display congratulatory/loser message
        _scoreboard is used to display scores"""
        if self._game.getBrickLength() == 0:
            self._wincomplete()
        else:
            self._losecomplete()
        self._ball = None
        
    def _level2(self):
        """Helper method to display message moving player onto level 2.
        Also resets score dictionary, game number, and timer."""
        self._mssg.text = str('LEVEL 2\n\nTwo balls will be served.\nPress'+
                ' any key if you dare.')
        self._done = None
        self._levelinput = 2
        self._scoredict = {}
        self._gamenum = 0
        self._timer = 0
        for x in range(0,5):
            self._scoreboard[x].text = ''
        self._score = None
    
    def _wincomplete(self):
        """Helper method for _complete.
        The player has successfully eliminated every brick.
        Displays congratulatory message if limit of 5
        turns has not been reached.
        Adds a score of total number of bricks to the scoreboard next to the
        number of the game/turn just used.
        Score are listed in chronological order with colors
        matching brick colors of active state."""
        self._mssg = GLabel(text='',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                                font_name='arcade')
        if self._gamenum < 5:
            self._mssg.text = str('Congratulations! You win!\nPress'+
                                      ' any key to play again\n\nScoreboard:')
        self._scoredict[self._gamenum] = str(self._game.getStoredBricks())
        for x in sorted(self._scoredict):
            self._scoreboard[self._gamenum - 1].text = str('Try: '
                                +str(x)+' ....... Points: '
                                +str(self._scoredict[x]))
        if self._gamenum == 5 and self._levelinput == 1:
            self._done = GLabel(
                text='Can you handle LEVEL 2?\nP'+
                'ress any key to continue',
                x=GAME_WIDTH/2, y = GAME_HEIGHT/2,
                font_name='arcade')
        elif (self._gamenum == 5) and (self._levelinput ==2):
            self._mssg = None
            self._done = GLabel(
                text = str('To go back to Level 1,\npress any key.'),
                x=GAME_WIDTH/2, y = GAME_HEIGHT/2,
                font_name='arcade')
            self._timer = 0
            
            
    
    def _losecomplete(self):
        """Helper method for _complete.
        The player eliminated only some of the bricks.
        Displays 'LOSER' message if limit of 5 turns has not
        been reached. Adds score of number of bricks eliminated to the
        scoreboard next to number of the game/turn just used.
        Score are listed in chronological order with colors
        matching brick colors of active state.
        This is used in instance of the player
        not eliminating all the bricks, but running out of tries."""
        self._mssg = GLabel(text='',x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                                font_name='arcade')
        if self._gamenum < 5:
            self._mssg.text = str('LOSER\nPress any'+
                                      ' key to play again\n\nScoreboard:')
        self._scoredict[self._gamenum] = str(
                self._game.getStoredBricks() - self._game.getBrickLength())
        for x in sorted(self._scoredict):
            self._scoreboard[self._gamenum - 1].text = str('Try: '
                        +str(x)+' ....... Points: '
                        +str(self._scoredict[x]))
        if (self._gamenum == 5) and (self._levelinput ==1):
            self._mssg.text = ''
            self._done = GLabel(
                text = str('Can you handle LEVEL 2?\nP'+
                        'ress any key to continue'),
                    x=GAME_WIDTH/2, y = GAME_HEIGHT/2,
                    font_name='arcade')
        elif (self._gamenum == 5) and (self._levelinput ==2):
            self._mssg = None
            self._done = GLabel(
                text = str('To go back to Level 1,\npress any key.'),
                x=GAME_WIDTH/2, y = GAME_HEIGHT/2,
                font_name='arcade')
            self._timer = 0
    
