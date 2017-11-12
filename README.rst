========
pyavagen
========

|build_badge| |versions_badge| |pypi_badge| |license_badge|

Generation of customizable avatars.

**Requirements:**

-  Python 3.3+
-  Pillow

**Installation:**

::

    pip install pyavagen

Avatar types
============

For avatar generation using the ``Avatar`` class.

**Arguments:**

-  ``kwargs`` - keyword arguments that are passed to specified avatar\_class.
-  ``avatar_type`` - avatar type that will be generates an image.

Types: 

1. ``pyavagen.SQUARE_AVATAR`` or ``'square'`` 
2. ``pyavagen.CHAR_AVATAR`` or ``'char'`` 
3. ``pyavagen.CHAR_SQUARE_AVATAR`` or ``'char_square'``

Avatar types description is given below.

Char avatar
===========

Draws a character on background with single color.

|Demo 4| |Demo 5| |Demo 10| |Demo 12|

**Usage:**

.. code:: python


    import pyavagen


    avatar = pyavagen.Avatar(pyavagen.CHAR_AVATAR, size=500, string="Paul")
    avatar.generate().save('avatar.png') 

**Arguments:**

-  ``size`` - size of output image. The integer type.
-  ``string`` - first chars of two first words that separated whitespaces.
   For example from string 'John Paul' draws "JP".
   If passed an one word then draws a first char of this word.
   For example from string 'John' draws "J". The string type.
-  ``font`` - TrueType or OpenType font file. Path to font file. Default
   Comfortaa-Regular.
-  ``background_color`` - background color. If not passed that a will be
   a random color from ``color_list``.
-  ``font_size`` - size of font. The integer type. Has default value.
-  ``font_color`` - color of font. The string type. Default white.
-  ``font_outline`` - Outline of character. Default false.
-  ``color_list`` - list of colors from which will be generating colors
   for background. Default ``pyavagen.COLOR_LIST_FLAT``.

Square avatar
=============

Draws squares with different colors.

|Demo 1| |Demo 2| |Demo 3| |Demo 11|

**Usage:**

.. code:: python


    import pyavagen


    avatar = pyavagen.Avatar(pyavagen.SQUARE_AVATAR, size=500)
    avatar.generate().save('avatar.png')

**Arguments:**

-  ``size`` - size of output image. The integer type.
-  ``squares_on_axis`` - number of squares on axis. The integer type.
   Default random value from 3 to 4.
-  ``blur_radius`` - blur radius. Used
   ``PIL.ImageFilter.GaussianBlur``.The integer type. Default 1.
-  ``rotate`` - image rotate. The integer type. Default random rotation.
-  ``border_size`` - border size of square. The integer type. Default 0.
-  ``border_color`` - border color of squares. The string type. Default
   black.
-  ``color_list`` - list of colors from which will be generating colors
   for squares. By default a set of flat colors
   (``pyavagen.COLOR_LIST_FLAT``). If ``color_list`` passed as an empty
   list then will be generation a random color. There is also list of
   colors in material style - ``pyavagen.COLOR_LIST_MATERIAL``.


Char square avatar
==================

Draws a character on background with squares with different colors.

|Demo 6| |Demo 7| |Demo 8| |Demo 9|

**Usage:**

.. code:: python


    import pyavagen


    avatar = pyavagen.Avatar(pyavagen.CHAR_SQUARE_AVATAR, size=500, string="Jack")
    avatar.generate().save('avatar.png') 

**Arguments:**

The same arguments as for Square avatar and Char avatar.

Testing
=======

Execute ``tox`` from the project root.

.. |Demo 1| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo1.png?raw=true
.. |Demo 2| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo2.png?raw=true
.. |Demo 3| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo3.png?raw=true
.. |Demo 11| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo11.png?raw=true
.. |Demo 4| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo4.png?raw=true
.. |Demo 5| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo5.png?raw=true
.. |Demo 10| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo10.png?raw=true
.. |Demo 12| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo12.png?raw=true
.. |Demo 6| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo6.png?raw=true
.. |Demo 7| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo7.png?raw=true
.. |Demo 8| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo8.png?raw=true
.. |Demo 9| image:: https://github.com/abalx/pyavagen/blob/master/examples/demo9.png?raw=true

.. |build_badge| image:: https://travis-ci.org/abalx/pyavagen.svg?branch=master
    :target: https://travis-ci.org/abalx/pyavagen


.. |license_badge| image:: https://img.shields.io/github/license/abalx/pyavagen.svg
    :target: https://github.com/abalx/pyavagen/blob/development/LICENSE
    
.. |pypi_badge| image:: https://img.shields.io/pypi/v/pyavagen.svg   
    :target: https://pypi.python.org/pypi/pyavagen/0.3.2

.. |versions_badge| image:: https://img.shields.io/pypi/pyversions/pyavagen.svg
