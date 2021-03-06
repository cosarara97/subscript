"""
These functions are imported into the global namespace of the script, and can
be called without any module prefix.
"""

import subscript.langtypes as langtypes
import subscript.script as script
import subscript.registry as registry

functions = registry.Registry('main')

# =========================================
# TODO: Missing functions
# =========================================


# TODO: Some functions end scripts
# Record which ones these are. (Possibly warp, warpmuted, etc.)
# - end
# - goto -- ends a section

# Functions in square brackets are present here, but should be reviewed

# Functions that should be implemented elsewhere
# Assignment type functions
# - writebytetooffset
# - loadbytefrompointer
# - setfarbyte
# - copyscriptbanks
# - loadpointer
# - setbyte
# - setbyte2
# - setfarbyte
# - copyscriptbanks
# - copybyte
# - setvar
# - addvar
# - subvar
# - copyvar
# - copyvarifnotzero
# - setflag
# - clearflag
# - resetvars
# - cleartrainerflag
# - settrainerflag

# Comparison type functions
# - comparebanks
# - comparebanktobyte
# - comparebanktofarbyte
# - comparefarbytetobank
# - comparefarbytetobyte
# - comparefarbytes
# - compare
# - comparevars
# - checkflag
# - checktrainerflag
# - checkattack

# Conditional commands
# - callstdif
# - gotostdif

# ----------------------------------------------

# Functions that should be in a submodule?

# Specials:
# - special
# - special2
# - waitstate

# Sounds:
# - playsong
# - playsong2
# - fadedefault
# - fadesong
# - fadeout
# - fadein
# - [fanfare]
# - [waitfanfare]
# - [sound]
# - [waitsound]

# ----------------------------------------------

# Nop functions

# - cmd2c
# - checkdailyflags

# ----------------------------------------------

@functions.register
def lock(script, lockall=False):
    '''
    If `lockall` is ``False``, and the script was called by a Person event, then
    that Person's movement will cease. Otherwise, the function locks all
    overworlds on-screen in place.

    :param lockall: Lock every overworld if ``True``
    '''
    if lockall:
        return ('lockall',)
    else:
        return ('lock',)

@functions.register
def message(script, string, keepopen=False):
    '''
    Displays message with text `string` in a message box. If `keepopen` is ``True``,
    the box will not close until :func:`closeonkeypress` is called.

    :param string: The message to display
    :param keepopen: Whether the box will stay open or close when the player presses a key
    '''
    out = []
    out.append(('loadpointer', 0, string.value))
    if keepopen:
        out.append(('callstd', 4))
    else:
        out.append(('callstd', 6))
    return out

@functions.register
def msgbox(script, string, keepopen=False):
    '''
    Alias for :func:`message`
    '''
    # An alias for message()
    return message.inner(string, keepopen)

@functions.register
def question(script, string):
    '''
    Displays `string` in a message box, and then displays a Yes/No selection box.
    If the player cancels or selects No, ``LASTRESULT`` is set to ``0``. Otherwise
    it is set to ``1``.

    :param string: The question to ask.
    '''
    out = []
    out.append(('loadpointer', 0, string.value))
    out.append(('callstd', 5))
    return out

@functions.register
def givepokemon(script, species, level=5, item=0):
    '''
    Add the Pokemon given by `species` to the player's party. If it is full,
    it is sent to the PC.

    :param species: The Pokemon to give.
    :param level: The level of the Pokmeon. Defaults to ``5``
    :param item: The item it will hold. Defaults to nothing.
    '''
    return ('givepokemon', species, level, item, 0, 0, 0)

@functions.register
def fanfare(script, sound):
    '''
    Plays the specified fanfare. Non-blocking.

    :param sound: The sound to play
    '''
    return ('fanfare', sound)

@functions.register
def waitfanfare(script):
    '''
    Blocks until function :func:`fanfare` has finished.
    '''
    return ('waitfanfare',)

@functions.register
def closeonkeypress(script):
    '''
    Closes a message that had the `keepopen` parameter set to ``True``.
    '''
    return ('closeonkeypress',)

@functions.register
def call(script, pointer):
    '''
    Jumps to destination and continues script execution from there.
    The location of the calling script is remembered and can be returned to later.

    The maximum script depth (that is, the maximum nested calls you can make) is
    20. When this limit is reached, the game starts treating call as goto

    :param pointer: The pointer to jump to
    '''
    return ('call', pointer)

@functions.register
def callstd(script, func):
    '''
    Calls a standard script function.

    :param func: The index of the function to call.
    '''
    return ('callstd', func)

@functions.register
def goto(script, destination):
    '''
    Jumps to `destination` and continues script execution from there.

    :param destination: Location to jump to.
    '''
    return ('goto', destination)

@functions.register
def gotostd(script, func):
    '''
    Jumps to the standard script function and continues execution from there.

    :param func:  The index of the function to call.
    '''
    return ('gotostd', func)

@functions.register
def pause(script, time):
    '''
    Blocks script execution for ``time``.

    :param time: The number of frame to wait
    '''
    return ('pause', time)

@functions.register
def release(script, doall=False):
    '''
    Reverses the effects of :func:`lock`.

    :param doall: Reverse the effects of :command:`lockall` or :command:`lock`.
    '''
    if doall:
        return ('releaseall',)
    else:
        return ('release',)

@functions.register
def additem(script, item, quantity=1):
    '''
    Silently add an item to the player's bag.

    :param item: The item to add.
    :param quanity: How many copies of `item` to give. Defaults to ``1``
    '''
    return ('additem', item, quantity)

@functions.register
def giveitem(script, item, quantity=1, fanfare=0):
    '''
    Gives the player an item, adding to to their bag while displaying a message
    and playing an optional sound.

    :param item: The item to add.
    :param quanity: How many copies of `item` to give. Defaults to ``1``.
    :param fanfare: The sound to play.
    '''
    out = []
    out.append(('copyvarifnotzero', 0x8000, item))
    out.append(('copyvarifnotzero', 0x8001, quantity))
    if fanfare > 0:
        out.append(('copyvarifnotzero', 0x8002, fanfare))
        out.append(('callstd', 9))
    else:
        out.append(('callstd', 0))
    return out

@functions.register
def givedecoration(script, decoration):
    '''
    :command:`nop` in FireRed
    '''
    out = []
    out.append(('copyvarifnotzero', 0x8000, decoration))
    out.append(('callstd', 7))
    return out

@functions.register
def finditem(script, item, quantity=1):
    '''
    Gives the player an item, adding to to their bag while displaying a message
    saying that they found the item.

    :param item: The item to add.
    :param quanity: How many copies of `item` to give. Defaults to ``1``.
    '''

    out = []
    out.append(('copyvarifnotzero', 0x8000, item))
    out.append(('copyvarifnotzero', 0x8001, quantity))
    out.append(('callstd', 1))
    return out

@functions.register
def wildbattle(script, species, level=70, item=0):
    '''
    Triggers a prefined wild Pokemon battle. Blocks until the battle finishes.

    :param species: The Pokemon to battle
    :param level: The level of the wild Pokemon. Defaults to 70 (Legendary)
    :param item: The item that the wild Pokemon holds.
    '''

    return [('setwildbattle', species, level, item), ('dowildbattle',)]

@functions.register
def jumpram(script):
    '''
    Executes a script stored in a default RAM location.
    '''
    return ('jumpram',)

@functions.register
def killscript(script):
    '''
    Executes a script stored in a default RAM location.
    '''
    return ('killscript',)

@functions.register
def setbyte(script, byte):
    '''
    Pads the specified value to a dword, and then writes that dword to a
    predefined address (0x0203AAA8).

    :param byte: Value to set
    '''
    return ('setbyte', byte)

@functions.register
def arm(script, pointer):
    '''
    Calls the ARM assembly routine stored at offset.

    :param pointer: Offset
    '''

    # Unset Thumb mode
    routine = pointer & ~(1)
    return ('callasm', routine)

@functions.register
def thumb(script, pointer):
    '''
    Calls the Thumb assembly routine stored at offset.

    :param pointer: Offset
    '''

    # Set Thumb mode
    routine = pointer | 1
    return ('callasm', routine)

@functions.register
def asm(script, pointer):
    '''
    Calls the assembly routine at the pointer, without setting the mode.

    :param pointer: Offset
    '''
    return ('callasm', pointer)

@functions.register
def loadthumb(script, pointer):
    '''
    Loads a Thumb routine into the script RAM.

    :param pointer: Offset
    '''
    return ('cmd24', pointer)

@functions.register
def sound(script, number):
    '''
    Plays the specified (sound_number) sound. Only one sound may play at a time, with newer ones interrupting older ones.

    If you specify sound 0x0000, then all music will be muted. If you specify the number of a non-existent sound, no new sound will be played, and currently-playing sounds will not be interrupted. A comprehensive list of sound numbers may be found on PokeCommunity.

    Note that when using older versions of VisualBoyAdvance, the sound channel used for this command (and, sometimes, in music) will be completely muted after loading from a savestate.

    :param sound: The number of the sound to play.
    '''
    return ('sound', number)

@functions.register
def waitsound(script, number):
    '''
    Blocks script execution until the currently-playing sound (triggered by sound) finishes playing.
    '''

    return ('checksound',)

@functions.register
def warp(script, bank=127, number=127, byte=127, x=0, y=0, style='normal'):
    '''
    Sends the player to Warp warp on Map bank.map. If the specified warp is 0xFF,
    then the player will instead be sent to (X, Y) on the map.
    This command will also play Sappy song 0x0009, but only if the bytes at 0x02031DD8 and 0x0203ADFA are not equal to 0x00 and 0x02, respectively.

    :param bank: The map bank to warp to.
    :param number: The map number in `bank` to warp to.
    :param byte: The number of the warp to go go.
    :param x: The x coordinate to go to. Can be a variable.
    :param y: The y coordinate to go to. Can be a variable.
    :param style: How to warp. Can be ``'normal'``, ``'mute'``, ``'walk'``, ``'teleport'``, ``'fall'``, ``'safari'``, ``'4'``, ``'5'`` or ``'set'``
    '''

    if style == 'normal':
        return ('warp', bank, number, byte, x, y)
    elif style == 'mute':
        return ('warpmuted', bank, number, byte, x, y)
    elif style == 'walk':
        return ('warpwalk', bank, number, byte, x, y)
    elif style == 'teleport':
        return ('warpteleport', bank, number, byte, x, y)
    elif style == 'fall':
        return ('warphole', bank, number)
    elif style == 'safari':
        return ('warp3', bank, number, byte, x, y)
    elif style == '4':
        return ('warp4', bank, number, byte, x, y)
    elif style == '5':
        return ('warp5', bank, number, byte, x, y)
    elif style == 'set':
        return ('setwarpplace', bank, number)

@functions.register
def getplayerpos(script, var_x, var_y):
    '''
    Retrieves the player's zero-indexed X- and Y-coordinates in the map, and stores them in the specified variables.

    :param var_x: The variable to store the X-coordinate in.
    :param var_y: The variable to store the Y-coordinate in.
    '''
    return (script, getplayerpos, var_x, var_y)

@functions.register
def countparty(script):
    '''
    Retrieves the number of Pokémon in the player's party, and stores that number in variable 0x800D (LASTRESULT).
    '''
    return ('countpokemon',)

@functions.register
def removeitem(script, item, quantity=1):
    '''
    Removes quantity of item index from the player's Bag.

    If you attempt to remove more of the item than the player actually has, then this command will do absolutely nothing, and they will keep the item.

    :param item: The item to remove.
    :param quantity: The amount of the item to remove. Defaults to ``1``.
    '''
    return ('removeitem', item, quantity)

@functions.register
def checkitemroom(script, item, quantity=1):
    '''
    Checks if the player has enough space in the Bag to hold `quantity` of `item`.
    If there is room, it sets variable 0x800D (``LASTRESULT``) to 0x0001, otherwise it is set to 0x0000.

    :param item: The item to check.
    :param quantity: The amount of the item to check. Defaults to ``1``.
    '''
    return ('checkitemroom', item, quantity)

@functions.register
def checkitem(script, item, quantity=1):
    '''
    Checks if the player has `quantity` or more of `item` in the Bag.
    Sets variable 0x800D (``LASTRESULT``) to 0x0001 if the player has enough of `item`, or 0x0000 if they have fewer than `quantity` of `item`.

    :param item: The item to check.
    :param quantity: The amount of item to check for. Defaults to ``1``.
    '''
    return ('checkitem', item, quantity)

# Skipped 0x48 because I wasn't sure how to implement right now.
# Skipped 0x49 & 0x4A -- missing from DavidJCobb's database

@functions.register
def adddecoration(script, decoration):
    '''
    In FR/LG, this command is a ``nop``. (The argument is read, but not used for anything.)

    :param decoration: The decoration to add.
    '''
    return ('addecoration', decoration)

@functions.register
def removedecoration(script, decoration):
    '''
    In FR/LG, this command is a ``nop``. (The argument is read, but not used for anything.)

    :param decoration: The decoration to remove.
    '''
    return ('removedecoration', decoration)

@functions.register
def checkdecorationroom(script, decoration):
    '''
    In FR/LG, this command is a ``nop``. (The argument is read, but not used for anything.)

    :param decoration: The decoration to check for.
    '''
    # Suggest: Renaming in command database?
    return ('testdecoration', decoration)

@functions.register
def checkdecoration(script, decoration):
    '''
    In FR/LG, this command is a ``nop``. (The argument is read, but not used for anything.)

    :param decoration: The decoration to check for.
    '''
    return ('checkdecoration', decoration)

@functions.register
def applymovement(script, movements, overworld=0xFF):
    '''
    Moves the overworld with Person ID `overworld` with the movement set
    `movements`. The function moves the player by default.

    :param movements: A list of the movements to use.
    :param overworld: The ID of the overworld to apply the movement to. Defaults to ``0xFF`` (``MOVE_PLAYER``)
    '''
    return ('applymovement', overworld, movements.value)

# 0x50 - applymovementpos is somewhat broken
@functions.register
def applymovementplayer(script, movements):
    '''
    Moves the player overworld with the movement set `movements`.

    :param movements: A lits of the movements to use.
    '''
    # Format: OW movements X Y
    # OW must be 0xFF, X and Y don't do anything
    return ('applymovementpos', 0xFF, movements, 0x0, 0x0)

@functions.register
def waitmovement(script, overworld=0x0):
    '''
    Blocks script execution until the movements being applied to the Person ID
    `overworld` finish.
    If `overworld` is ``0x0000``, the execution will wait until all overworlds
    affected finish.

    :param overworld: The ID of the overworld to wait for. Defaults to ``0x0000``
    '''
    return ('waitmovement', overworld)

@functions.register
def waitmovementplayer(script):
    '''
    A clone of :func:`waitmovement` that only works with the player overworld.
    '''
    # Format: OW X Y
    # Only works if OW = 0xFF, X and Y have no effect
    return ('waitmovementpos', 0xFF, 0x0, 0x0)

@functions.register
def disappear(script, sprite):
    '''
    Hides the overworld with ID ``sprite``

    :param sprite: The ID of the overworld to hide.
    '''

    return ('hidesprite', sprite)

@functions.register
def hide(script, sprite):
    '''
    An alias for :func:`disappear`.
    '''
    return disappear.inner(sprite)

# TODO: 0x54 hidespritepos
# Commands 0x55 - 0x59 are missing

@functions.register
def faceplayer(script):
    '''
    If the script was called by a Person event, then that Person will turn to
    face the tile that the player is stepping off of.
    '''
    return ('faceplayer',)

# Command 0x5B is also missing

# TODO: 0x5C trainerbattle
@functions.register
def repeattrainerbattle(script):
    '''
    Starts a trainer battle using the battle information stored in RAM (usually
    by trainerbattle, which actually calls this command behind-the-scenes), and
    blocks script execution until the battle finishes.
    '''
    return ('repeattrainerbattle',)

# Missing 0x5E - 0x65

@functions.register
def waitmsg(script):
    '''
    If a standard message box (or its text) is being drawn on-screen, this
    command blocks script execution until the box and its text have been fully
    drawn.
    '''
    return ('waitmsg',)

@functions.register
def preparemsg(script, message):
    '''
    Starts displaying a standard message box containing the specified text. If
    text is a pointer, then the string at that offset will be loaded and used.
    If text is script bank 0, then the value of script bank 0 will be treated
    as a pointer to the text. (You can use loadpointer to place a string pointer
    in a script bank.)

    :param message: The message to display.
    '''
    return ('preparemsg', message.value)

@functions.register
def waitkeypress(script):
    '''
    Blocks script execution until the player presses any key.
    '''
    return ('waitkeypress',)

@functions.register
def yesnobox(script, x, y):
    '''
    Displays a YES/NO multichoice box at the specified coordinates, and blocks
    script execution until the user makes a selection. Their selection is stored
    in variable 0x800D (LASTRESULT); 0x0000 for "NO" or if the user pressed B,
    and 0x0001 for "YES".

    :param x: The x coordinate on the screen.
    :param y: The y coordinate on the screen.
    '''
    return ('yesnobox',)

@functions.register
def multichoice(script, x, y, choices, cancel=1, default=None, per_row=-1):
    '''
    Displays a multichoice box from which the user can choose a selection, and
    blocks script execution until a selection is made. Lists of options are
    predefined and the one to be used is specified with list.


    '''

    # TODO: Allow editing and adding mutlichoice lists from the editor
    # TODO: Check that per_row is valid from the table of multichoice boxes
    if per_row != -1:
        if default == None:
            return ('multichoice3', x, y, choices, default, cancel)
        else:
            # TODO: Emulate default functionality. For that, we'll need to allow
            # Commands to add sections. (Alter compile to allow 'section' type
            # to be returned
            raise Exception('Cannot use default and per_row')
    else:
        if default == None:
            return ('multichoice', x, y, choices, cancel)
        else:
            return ('multichoice2', x, y, choices, default, cancel)

# Missing 0x71 - 0x74

@functions.register
def showpokepic(script, species, x, y):
    '''
    Displays a box containing the front sprite for the specified (species)
    Pokémon species.

    :param species: The species to show.
    :param x: The x-coordinate.
    :param y: The y-coordinate.
    '''

    return ('showpokepic', species, x, y)

@functions.register
def hidepokepic(script):
    '''
    Hides all boxes displayed with showpokepic.
    '''
    return ('hidepokepic',)

# 0x77 is a nop

# 0x78 is more complicated. Should look at braille text examples and automatically
# convert to the proper commands

# The buffer pokemon commands have the é symbol in them. Fix this up
@functions.register
def bufferpoke(script, buffer, species):
    '''
    Writes the name of the Pokémon at index species to the specified buffer.

    :param buffer: The script buffer to write to.
    :param species: The Pokemon name to buffer.
    '''
    return ('bufferPokémon', buffer, species)

@functions.register
def bufferfirstpoke(script, buffer):
    '''
    Writes the name of the first Pokémon in the player's party to the specified buffer.

    :param buffer: The buffer to write the name to.
    '''

    return ('bufferfirstPokémon', buffer)

# Finished up to command number 0x7E
# Resume from http://www.sphericalice.co/romhacking/davidjcobb_script/#c-7F

