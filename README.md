# Flappy Bird - Pygame Tutorial
### Year 10 Software Engineering

You will build Flappy Bird across **4 lessons**. Each lesson adds a new feature to the game. By the end you'll have a fully working game with a scrolling background, animated bird, pipes, scoring, and a restart button.

Open `FlappyBirdGame.py` to start. This is your working file.

---

## Lesson 1 - The Game Window

**What you'll add:** a clock, a background image, and a scrolling ground.

Open `FlappyBirdGame.py`. You'll see it already creates a window and runs a basic game loop. Your job is to build on top of it.



### Step 1 - Add a clock

A clock controls how fast the game runs (frames per second). Without it, the game runs as fast as your computer allows - which is too fast.

Find this line near the top of your file:
```python
pygame.init()
```

Directly underneath it, add:
```python
clock = pygame.time.Clock()
fps = 60
```

Then find the line at the top of your `while` loop:
```python
while run:
```

Add this as the **very first line inside the loop** (indented):
```python
    clock.tick(fps)
```

This tells Pygame: "wait here until 1/60th of a second has passed before doing the next frame."

---

### Step 2 - Load the background and ground images

Images need to be loaded **before** the game loop. Find the line:
```python
pygame.display.set_caption('Flappy Bird')
```

After it, add:
```python
# Load images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
```

> **Note:** The images are stored in a folder called `img/`. This is why we write `'img/bg.png'` not just `'bg.png'`.

---

### Step 3 - Draw the background

Inside your game loop, you need to draw the background every frame. Find the event loop inside your `while` loop:
```python
    for event in pygame.event.get():
```

Add these lines **above** the for loop:
```python
    # Draw background
    screen.blit(bg, (0, 0))
```

`screen.blit(image, (x, y))` draws an image at position x, y on the screen. The top-left corner is `(0, 0)`.

---

### Step 4 - Add a scrolling ground

The ground scrolls sideways to give the feeling of movement. Add these two variables before your game loop (near where you loaded the images):
```python
ground_scroll = 0
scroll_speed = 4
```

Then inside your game loop, after the `screen.blit(bg, ...)` line you just added, add:
```python
    # Draw the ground
    screen.blit(ground, (ground_scroll, 700))

    # Scroll the ground left each frame
    ground_scroll -= scroll_speed

    # Reset the scroll so it loops seamlessly
    if abs(ground_scroll) > 35:
        ground_scroll = 0
```

**How it works:**
- Every frame, `ground_scroll` decreases by 4 - moving the ground image left.
- `abs()` gives the absolute (positive) value of a number. When the ground has moved 35 pixels left, we snap it back to 0. Because the ground image is designed to tile, this looks seamless.

---

### Lesson 1 Check

Run your game. You should see:
- [ ] The background image fills the screen
- [ ] The ground appears at the bottom and scrolls left
- [ ] The window stays open until you close it

Compare your file with `FlappyBirdGame.py` - they should now look the same.

---

## Lesson 2 - The Bird Class

**What you'll add:** a `Bird` class that loads images, falls under gravity, flaps when clicked, and animates.

### What is a class?

A class is a blueprint for an object. Our `Bird` class bundles together:
- The bird's **data** (position, speed, images) - called *attributes*
- The bird's **behaviour** (falling, flapping, animating) - called *methods*

Once we define the class, we create one bird object: `flappy = Bird(100, 450)`.

---

### Step 5 - Create the Bird class

Add the following class definition **before** your game loop but **after** your image loading. Type it out carefully - indentation matters in Python.

```python
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
```

**What each part does:**

| Line | What it does |
|---|---|
| `class Bird(pygame.sprite.Sprite):` | Creates the Bird class, inheriting from Pygame's built-in Sprite class |
| `def __init__(self, x, y):` | The constructor - runs when you create a Bird object |
| `self.images = []` | An empty list that will hold the 3 bird animation frames |
| `for num in range(1, 4):` | Loops through numbers 1, 2, 3 |
| `pygame.image.load(f'img/bird{num}.png')` | Loads bird1.png, bird2.png, bird3.png |
| `self.images.append(img)` | Adds each image to the list |
| `self.rect.center = [x, y]` | Places the bird at position (x, y) |
| `self.vel = 0` | Starting velocity - 0 means not moving yet |
| `self.clicked = False` | Prevents the bird from flapping repeatedly on one click |

---

### Step 6 - Add the update method

The `update()` method runs every frame. It handles gravity, flapping, and animation. Add this **inside** the Bird class (indented one level):

```python
    def update(self):
        # Apply gravity - vel increases each frame
        self.vel += 0.6
        if self.vel > 5:
            self.vel = 5    # cap the falling speed

        # Move the bird down (but not through the ground)
        if self.rect.bottom < 700:
            self.rect.y += int(self.vel)

        # Flap when the mouse is clicked
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10      # negative velocity = moving up
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Animation - cycle through the 3 images
        flap_cooldown = 5
        self.counter += 1
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        # Rotate the bird based on velocity
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
```

**How gravity works:**
- `self.vel` starts at 0
- Each frame we add 0.6 - so it gets faster and faster (like real gravity)
- We cap it at 5 so the bird doesn't fall infinitely fast
- We add `self.vel` to `self.rect.y` - this moves the bird down the screen

**How flapping works:**
- `pygame.mouse.get_pressed()[0]` is `1` when the left mouse button is held down
- When clicked, we set `self.vel = -10` - a large negative number makes the bird move UP
- `self.clicked` prevents this from firing every frame while the button is held

**How animation works:**
- `self.counter` goes up by 1 every frame
- When it passes `flap_cooldown` (5), we move to the next image and reset the counter
- After image 3, we wrap back to image 1

---

### Step 7 - Create the bird and add it to a sprite group

After your class definition, add:
```python
bird_move = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_move.add(flappy)
```

A **sprite group** is Pygame's way of managing multiple sprites at once. Even though we only have one bird, we use a group because it lets us call `draw()` and `update()` on everything in the group in one line.

---

### Step 8 - Draw and update the bird in the game loop

Inside your game loop, after `screen.blit(bg, (0, 0))`, add:
```python
    bird_move.draw(screen)
    bird_move.update()
```

Make sure this comes **before** the ground draw so the bird appears on top of the ground.

---

### Lesson 2 Check

Run your game. You should see:
- [ ] The bird appears in the middle of the screen
- [ ] It falls under gravity immediately
- [ ] Clicking the mouse makes it flap upward
- [ ] The bird animates (wings flap)
- [ ] The bird rotates to face the direction it's moving

---

## Lesson 3 - Pipes, Score & Game Over

**What you'll add:** pipes that scroll in, collision detection, a score counter, and a `flying` state so the game doesn't start until the first click.

---

### Step 9 - Add new game variables

Before your game loop, add these variables (after your existing image loading):
```python
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500    # milliseconds between each new pipe
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
```

Also load two more images:
```python
button_img = pygame.image.load('img/restart.png')
```

And add a font for the score:
```python
font = pygame.font.SysFont('ComicSans', 60)
white = (255, 255, 255)
```

---

### Step 10 - Add the draw_text function

This function makes it easy to draw text on screen. Add it before the class definitions:
```python
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
```

---

### Step 11 - Update the Bird class for the flying/game_over states

Your Bird's `update()` method needs to know about `flying` and `game_over`. Update it so that:
- Gravity only applies `if flying == True`
- Flapping and animation only happen `if game_over == False`
- When game over, the bird rotates to face down (`-90` degrees)

Here is the updated `update()` method - replace your existing one:

```python
    def update(self):
        if flying == True:
            # Apply gravity
            self.vel += 0.6
            if self.vel > 5:
                self.vel = 5
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Flap on click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animation
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # Rotate based on velocity
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # Point bird at the ground when dead
            self.image = pygame.transform.rotate(self.images[self.index], -90)
```

---

### Step 12 - Add the Pipe class

Add this after the Bird class:

```python
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 = top pipe (flipped upside down)
        # position -1 = bottom pipe (normal orientation)
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 1.5)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 1.5)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
```

**How pipes are positioned:**
- Each time a pipe spawns, we pick a random `y` value for the centre of the gap
- The top pipe's **bottom** edge sits above the gap: `y - pipe_gap / 1.5`
- The bottom pipe's **top** edge sits below the gap: `y + pipe_gap / 1.5`
- `self.kill()` removes the pipe from all sprite groups when it goes off screen

---

### Step 13 - Add the Button class

```python
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
```

`collidepoint(pos)` checks whether the mouse position is inside the button's rectangle. If it is AND the mouse is clicked, `action` becomes `True`.

---

### Step 14 - Add the reset_game function

Add this before the game loop:
```python
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score
```

---

### Step 15 - Create sprite groups and the button

Replace your old `bird_move` group lines with:
```python
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)
```

---

### Step 16 - Update the game loop

Replace your entire `while run:` loop with the following. Read the comments carefully - each block has a specific job:

```python
run = True
while run:
    clock.tick(fps)

    # 1. Draw background and sprites
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # 2. Draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))

    # 3. Check the score - did the bird pass a pipe?
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # 4. Check for collisions
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    # 5. Spawn and move pipes (only when flying and not game over)
    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        pipe_group.update()

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # 6. Show restart button if game over
    if game_over == True:
        if button.draw():
            game_over = False
            score = reset_game()

    # 7. Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
```

**How scoring works:**
- `pass_pipe` becomes `True` when the bird is between the left and right edges of the first pipe
- Once the bird's left side passes the pipe's right side, we add 1 to the score and reset `pass_pipe`

**How collision works:**
- `pygame.sprite.groupcollide(bird_group, pipe_group, False, False)` checks if any bird sprite overlaps any pipe sprite
- The two `False` arguments mean "don't delete either sprite when they collide"

---

### Lesson 3 Check

Run your game. You should see:
- [ ] The bird sits still until the first click
- [ ] Pipes scroll in from the right after you click
- [ ] Hitting a pipe or the ground ends the game
- [ ] The score increases when you fly through a gap
- [ ] The restart button appears on game over

Your file should now match `FlappyBirdGame - Final.py` exactly.

---

### Lesson 4 - High score (File I/O)
Save the highest score to `assets/highscore.txt` so it persists between sessions.

```python
# Reading the high score
def load_high_score():
    try:
        with open('assets/highscore.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Saving a new high score
def save_high_score(score):
    with open('assets/highscore.txt', 'w') as f:
        f.write(str(score))
```

Call `load_high_score()` before the game loop. Call `save_high_score(score)` inside `reset_game()` if the new score beats the old one. Display both scores on screen using `draw_text()`.

---

## Lesson 5 - Extension Tasks

Pick one or more of the following to extend your game.

### Extension A - Difficulty scaling
Make the game harder the longer you survive. Inside the pipe-spawning block, after `score` increases, try:
```python
scroll_speed = 4 + score // 5   # speed increases every 5 points
```

---

### Extension B - Sound effects
Pygame can play short sound effects. Add these near your image loading:
```python
flap_sound = pygame.mixer.Sound('sounds/flap.wav')
hit_sound  = pygame.mixer.Sound('sounds/hit.wav')
```

Then call `flap_sound.play()` in the Bird's flap code, and `hit_sound.play()` when `game_over` is set to `True`.

---

### Extension C - Display a "best score" on the game over screen
When the game ends, show both the current score and the all-time best in large text before the restart button appears.
