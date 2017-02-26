# simple-avatar-generator

It is simple avatar generator. It may be useful for example for chats.

Creates a picture that has squares with different colors and rotation.

### Demo

![Demo 1](examples/demo1.png?raw=true "Demo 1")
![Demo 2](examples/demo2.png?raw=true "Demo 2")

### Requirements

- Python 3.6
- Pillow

### Using

    avatar = AvatarGenerator(
        side_sizes=800, 
        squares_quantity_on_axis=4
    ).generate()
    
    avatar.save('output.png')
    
The AvatarGenerator class takes two arguments:

1. **side_sizes** - size of sides for generated squares. The value measured in pixels.

2. **squares_quantity_on_axis** - quantity of squares on axis. For example if squares_quantity_on_axis value is 4, that total squares on generated picture be 16.

### Methods

**generate()** - generates a picture.

**save(filename='output.png')** - saves a picture on the disk. Takes an one argument - **filename**.

**show()** - this method from PIL. Provides a ability to view a picture.
