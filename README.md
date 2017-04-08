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
import pyavagen


pyavagen.Avatar(avatar_class, **kwargs)
```
    
#### Arguments   

- `avatar_class` - avatar class that will be generates an image.

Classes:
1. pyavagen.Avatar.SQUARE
2. pyavagen.Avatar.CHAR
3. pyavagen.Avatar.CHAR_SQUARE

Their description is given below.

- `kwargs` - keyword arguments that are passed to specified avatar_class.

## Square avatar

#### Description

Draws squares with different colors.

#### Demo

![Demo 1](examples/Demo1.png?raw=true "Demo 1")
![Demo 2](examples/Demo2.png?raw=true "Demo 2")
![Demo 3](examples/Demo3.png?raw=true "Demo 3")

#### Usage

```python

import pyavagen


pyavagen.Avatar(pyavagen.Avagen.SQUARE, size=500).generate().save('avatar.png') 
```

#### Arguments

- `size` - size of output image. The integer type. 
- `squares_quantity_on_axis` - number of squares on axis. The integer type. Default random value from 3 to 4. 
- `blur_radius` - blur radius. Used `PIL.ImageFilter.GaussianBlur`.The integer type. Default 1.
- `rotate` - image rotate. The integer type. Default random rotation.
- `square_border` - border color of squares. The string type.
- `color_list` - list of colors from which will be generating colors for squares. <br/>
 By default a set of flat colors (`pyavagen.COLOR_LIST_FLAT`). If `color_list` passed as an empty list then will be generation a random color. There is also list of colors in material style - `pyavagen.COLOR_LIST_MATERIAL`.



## Char avatar

#### Description

Draws a character on background with single color.

#### Demo

![Demo 4](examples/Demo4.png?raw=true "Demo 4")
![Demo 5](examples/Demo5.png?raw=true "Demo 5")

#### Usage

```python

import pyavagen


pyavagen.Avatar(pyavagen.Avatar.CHAR, size=500, string="Paul").generate().save('avatar.png') 
```

#### Arguments

- `size` - size of output image. The integer type.
- `string` - string, the first character of which will be used for displaying on generated image. The string type.
- `font` - TrueType or OpenType font file. Path to font file. Default Comfortaa-Regular.
- `background_color` - background color. If not passed that a will be a random color from `color_list`.
- `font_size` - size of font. The integer type. Has default value.
- `font_color` - color of font. The string type. Default white.
- `color_list` - list of colors from which will be generating colors for background. Default `pyavagen.COLOR_LIST_FLAT`.


## Char square avatar

#### Description

Draws a character on background with squares with different colors.

#### Demo

![Demo 6](examples/Demo6.png?raw=true "Demo 6")
![Demo 7](examples/Demo7.png?raw=true "Demo 7")
![Demo 8](examples/Demo8.png?raw=true "Demo 8")
![Demo 9](examples/Demo9.png?raw=true "Demo 9")

#### Usage

```python

import pyavagen


pyavagen.Avatar(pyavagen.Avatar.CHAR_SQUARE, size=500, string="Jack").generate().save('avatar.png') 
```

#### Arguments

The same arguments as for Square avatar and Char avatar.
