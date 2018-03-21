from SlidingTile import Slider
import pygame


# SliderRenderer renders a Slider object
class SliderRenderer:

    # initialises renderer
    def __init__(self, slider: Slider, block_size: int):

        # sets initial slider and the slider it is compared to to determine completion
        self.slider = slider
        self.complete = Slider(slider.width, slider.height, False)

        # block_size determines how large the sliding tile game is rendered
        self.block_size = block_size

        # sets the display size to the appropriate size
        self.display = (self.slider.width * block_size, self.slider.height * block_size)

        # initializes pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.display)
        pygame.display.set_caption('Sliding Puzzle')

        # sets font
        self.font = pygame.font.SysFont('Calibri', int(block_size * 0.7))
        self.render_grid()
        self.event_loop()

    # define the event loop
    def event_loop(self):
        pygame.display.flip()

        # Event loop
        while True:

            # gets all recent events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # defines moves on the release of a click
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # calculates the tile that is clicked on
                    loc = (int((pos[0] - pos[0] % self.block_size)/self.block_size),
                           int((pos[1] - pos[1] % self.block_size)/self.block_size))

                    # attempts to slide the selected tile
                    self.slider.move(loc[0]+1, loc[1]+1)
                    self.render_grid()
                    pygame.display.flip()

                    # checks if game is won
                    if self.slider.vals == self.complete.vals:

                        # generates completion message
                        self.font = pygame.font.SysFont('Calibri', int(self.block_size * 0.5))
                        text = self.font.render('Completed in '+str(self.slider.moves)+' moves', False, (255,)*3)
                        coord = text.get_rect(center=tuple(x/2 for x in self.display))
                        self.screen.blit(text, coord)

                        # updates screen
                        pygame.display.flip()

                        # next click closes the display
                        while True:
                            for end_event in pygame.event.get():
                                if end_event.type == pygame.MOUSEBUTTONUP:
                                    pygame.quit()
                                    quit()

    # renders the grid
    def render_grid(self):

        # blacks out the screen
        self.screen.fill((0, 0, 0))

        # loops over every cell
        for i in range(self.slider.width):
            for j in range(self.slider.height):

                # checks if the tile is the blank tile
                if self.slider.vals[i + 1, j + 1] != 0:

                    # draws filled square
                    pygame.draw.rect(self.screen, (150,)*3, [self.block_size * x for x in [i, j, i + 1, j + 1]])

                    # draws number
                    text = self.font.render(str(self.slider.vals[i + 1, j + 1]), False, (0, 0, 0))
                    coord = text.get_rect(center=(self.block_size * (i + 0.5), self.block_size * (j + 0.5)))
                    self.screen.blit(text, coord)

                else:

                    # draws square
                    pygame.draw.rect(self.screen, (0, 0, 0), [self.block_size * x for x in [i, j, i + 1, j + 1]])

                # draws border square
                pygame.draw.rect(self.screen, (0, 0, 0), [self.block_size * x for x in [i, j, i + 1, j + 1]], 2)


# if script directly run create a new game
if __name__ == "__main__":
    width = int(input('Enter game width: '))
    height = int(input('Enter game height: '))
    S = SliderRenderer(Slider(width, height, True), 50)
