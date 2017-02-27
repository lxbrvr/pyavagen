# simple-avatar-generator

It is simple avatar generator. It may be useful for example for chats.

Creates a picture that has squares with different colors and rotation.

### Demo

![Demo 1](examples/demo1.png?raw=true "Demo 1")
![Demo 2](examples/demo2.png?raw=true "Demo 2")
![Demo 3](examples/demo3.png?raw=true "Demo 3")
![Demo 4](examples/demo4.png?raw=true "Demo 4")

### Requirements

- Python 3.6
- Pillow

### Using

    avatar = AvatarGenerator(side_sizes=800).generate()
    avatar.save('output.png')
    
The AvatarGenerator class takes some arguments:

1. **side_sizes** - required. <br/>
Size of sides for generated squares. <br/>
The value measured in pixels. <br/>
Min value is 4.

2. **squares_quantity_on_axis** - optional. <br/>
By default random number from 3 to 4. <br/>
For example if squares_quantity_on_axis value is 4, that total squares on generated picture be 16.<br/>
Min value is 1.

3. **blur_radius** - optional. <br/>
By default 3. <br/>
Min value is 0.  

4. **rotate** - optional.<br/>
By default random number from 0 to 360.

5. **border** - optional.<br/>
By default black color.<br/>
Draws squares border. <br/>
Do `border=''` that remove border.


### Methods

**generate()** - generates a picture. Returns the PIL Image object.
