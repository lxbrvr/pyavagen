# pyavagen

Generation different type avatars with possibility customization.

### Requirements

- Python 3.6
- Pillow

### Installation

    pip install pyavagen


# Avatar types

For avatar generation using the `Avagen` class.

```python
from pyavagen import Avagen  
```
    
#### Arguments   

- `avatar_class` - avatar class that will be generates an image.

Classes:
1. Avagen.SQUARE
2. Avagen.CHAR
3. Avagen.CHAR_SQUARE

Their description is given below.

- `kwargs` - keyword arguments that are passed to specified avatar_class.

## Square avatar

#### Desription

Draws squares with different colors.

#### Demo

![Demo 1](examples/Demo1.png?raw=true "Demo 1")
![Demo 2](examples/Demo2.png?raw=true "Demo 2")
![Demo 3](examples/Demo3.png?raw=true "Demo 3")

#### Usage

```python

from pyavagen import Avagen


Avagen(Avagen.SQUARE, size=500).generate().save('avatar.png') 
```

#### Arguments

- `size` - size of output image. The integer type. 
- `squares_quantity_on_axis` - number of squares on axis. The integer type. Has a default value. 
- `blur_radius` - blur radius. The integer type.
- `rotate` - image rotate. The integer type. Has a default value.
- `square_border` - border color of squares. The string type.


## Char avatar

#### Desription

Draws a character on background with single color.

#### Demo

![Demo 4](examples/Demo4.png?raw=true "Demo 4")
![Demo 5](examples/Demo5.png?raw=true "Demo 5")

#### Usage

```python

from pyavagen import Avagen


Avagen(Avagen.CHAR, size=500, string="Paul").generate().save('avatar.png') 
```

#### Arguments

- `size` - size of output image. The integer type.
- `string` - string, the first character of which will be used for displaying on generated image. The string type.
- `font` - TrueType or OpenType font file. Path to font file. Has default value.
- `background_color` - background color. If is None that will be generated a random color.
- `font_size` - size of font. The integer type. Has default value.


## Char square avatar

#### Desription

Draws a character on background with squares with different colors.

#### Demo

![Demo 6](examples/Demo6.png?raw=true "Demo 6")
![Demo 7](examples/Demo7.png?raw=true "Demo 7")
![Demo 8](examples/Demo8.png?raw=true "Demo 8")
![Demo 9](examples/Demo9.png?raw=true "Demo 9")

#### Usage

```python

from pyavagen import Avagen


Avagen(Avagen.CHAR_SQUARE, size=500, string="Jack").generate().save('avatar.png') 
```

#### Arguments

The same arguments as for Square avatar and Char avatar.
