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


pyavagen.Avatar(avatar_type, **kwargs)
```
    
#### Arguments   

- `avatar_type` - avatar type that will be generates an image.

Types:
1. `pyavagen.SQUARE_AVATAR` or `'square'` 
2. `pyavagen.CHAR_AVATAR` or `'char'`
3. `pyavagen.CHAR_SQUARE_AVATAR` or `'char_square'`

Avatar types description is given below.

- `kwargs` - keyword arguments that are passed to specified avatar_class.

## Square avatar

#### Description

Draws squares with different colors.

#### Demo

![Demo 1](examples/Demo1.png?raw=true "Demo 1")
![Demo 2](examples/Demo2.png?raw=true "Demo 2")
![Demo 3](examples/Demo3.png?raw=true "Demo 3")
![Demo 11](examples/Demo11.png?raw=true "Demo 11")

#### Usage

```python

import pyavagen


avatar = pyavagen.Avatar(pyavagen.SQUARE_AVATAR, size=500)
avatar.generate().save('avatar.png')
```

#### Arguments

- `size` - size of output image. The integer type. 
- `squares_quantity_on_axis` - number of squares on axis. The integer type. Default random value from 3 to 4. 
- `blur_radius` - blur radius. Used `PIL.ImageFilter.GaussianBlur`.The integer type. Default 1.
- `rotate` - image rotate. The integer type. Default random rotation.
- `border_size` - border size of square. The integer type. Default 0.
- `border_color` - border color of squares. The string type. Default black.
- `color_list` - list of colors from which will be generating colors for squares. <br/>
 By default a set of flat colors (`pyavagen.COLOR_LIST_FLAT`). If `color_list` passed as an empty list then will be generation a random color. There is also list of colors in material style - `pyavagen.COLOR_LIST_MATERIAL`.



## Char avatar

#### Description

Draws a character on background with single color.

#### Demo

![Demo 4](examples/Demo4.png?raw=true "Demo 4")
![Demo 5](examples/Demo5.png?raw=true "Demo 5")
![Demo 10](examples/Demo10.png?raw=true "Demo 10")

#### Usage

```python

import pyavagen


avatar = pyavagen.Avatar(pyavagen.CHAR_AVATAR, size=500, string="Paul")
avatar.generate().save('avatar.png') 
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


avatar = pyavagen.Avatar(pyavagen.CHAR_SQUARE_AVATAR, size=500, string="Jack")
avatar.generate().save('avatar.png') 
```

#### Arguments

The same arguments as for Square avatar and Char avatar.
