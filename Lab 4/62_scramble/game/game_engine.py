import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = [
            "PYTHON",
            "PYGAME",
            "PLANET",
            "ROCKET",
            "GALAXY",
            "STREAM",
            "PUZZLE",
            "ALGORITHM"
        ]

        self.secret_word = ""
        self.scrambled_word = ""

        self.score = 0

        self.revealed_letters = []
        self.hint_penalty = 0.5

        self.round_time = 20
        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()

        self.tile_letters = []
        self.tile_rects = []
        self.selected_tile = None

        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        self.input_box = TextBox(
            width // 2 - 130,
            250,
            160,
            46
        )

        self.submit_btn = pygame.Rect(
            width // 2 + 45,
            250,
            95,
            46
        )

        self.hint_btn = pygame.Rect(
            width // 2 + 150,
            250,
            80,
            46
        )

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)
        self.font_tile = pygame.font.SysFont(None, 38)

        self.next_round()

    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            if shuffled != word or len(word) <= 1:
                return shuffled

    def create_tiles(self):
        self.tile_rects = []

        tile_size = 55
        gap = 8

        total_width = (
            len(self.tile_letters) * tile_size
            + (len(self.tile_letters) - 1) * gap
        )

        start_x = self.width // 2 - total_width // 2
        y = 155

        for i in range(len(self.tile_letters)):
            x = start_x + i * (tile_size + gap)

            rect = pygame.Rect(
                x,
                y,
                tile_size,
                tile_size
            )

            self.tile_rects.append(rect)

    def next_round(self):
        self.secret_word = random.choice(self.words)

        self.scrambled_word = self.scramble_string(
            self.secret_word
        )

        self.tile_letters = list(self.scrambled_word)

        self.revealed_letters = [
            False
        ] * len(self.secret_word)

        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()

        self.selected_tile = None

        self.create_tiles()

        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        self.input_box.clear()

    def get_tile_word(self):
        return "".join(self.tile_letters)

    def submit_guess(self):
        guess = self.get_tile_word()

        if not guess:
            self.feedback_msg = "Arrange the letters before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1

            self.feedback_msg = (
                f"CORRECT! '{self.secret_word}' is right."
            )

            self.feedback_color = (80, 230, 110)

            pygame.display.flip()
            pygame.time.delay(700)

            self.next_round()

        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)

            self.input_box.clear()

    def use_hint(self):
        for i, revealed in enumerate(self.revealed_letters):
            if not revealed:
                self.revealed_letters[i] = True

                self.score = max(
                    0,
                    self.score - self.hint_penalty
                )

                self.feedback_msg = (
                    f"Hint revealed: {self.secret_word[i]}"
                )

                self.feedback_color = (255, 220, 80)

                return

        self.feedback_msg = (
            "All letters have already been revealed!"
        )

        self.feedback_color = (255, 220, 80)

    def handle_tile_click(self, mouse_pos):
        clicked_tile = None

        for i, rect in enumerate(self.tile_rects):
            if rect.collidepoint(mouse_pos):
                clicked_tile = i
                break

        if clicked_tile is None:
            return

        if self.selected_tile is None:
            self.selected_tile = clicked_tile
            return

        if self.selected_tile == clicked_tile:
            self.selected_tile = None
            return

        first = self.selected_tile
        second = clicked_tile

        self.tile_letters[first], self.tile_letters[second] = (
            self.tile_letters[second],
            self.tile_letters[first]
        )

        self.selected_tile = None

        self.create_tiles()

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()
                    return

                if self.hint_btn.collidepoint(event.pos):
                    self.use_hint()
                    return

                for i, rect in enumerate(self.tile_rects):
                    if rect.collidepoint(event.pos):
                        self.handle_tile_click(event.pos)
                        return

        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()

    def update(self):
        current_time = pygame.time.get_ticks()

        elapsed_seconds = (
            current_time - self.last_time
        ) / 1000

        if elapsed_seconds >= 1:
            seconds_passed = int(elapsed_seconds)

            self.time_left -= seconds_passed
            self.last_time = current_time

            if self.time_left <= 0:
                self.time_left = 0

                self.feedback_msg = (
                    f"TIME'S UP! The word was '{self.secret_word}'."
                )

                self.feedback_color = (240, 80, 80)

                pygame.display.flip()
                pygame.time.delay(1000)

                self.next_round()

    def render_tiles(self, screen):
        for i, letter in enumerate(self.tile_letters):

            rect = self.tile_rects[i]

            if i == self.selected_tile:
                tile_color = (80, 130, 220)
            else:
                tile_color = (55, 65, 80)

            pygame.draw.rect(
                screen,
                tile_color,
                rect,
                border_radius=7
            )

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                rect,
                width=2,
                border_radius=7
            )

            letter_surface = self.font_tile.render(
                letter,
                True,
                (255, 255, 255)
            )

            screen.blit(
                letter_surface,
                (
                    rect.centerx
                    - letter_surface.get_width() // 2,
                    rect.centery
                    - letter_surface.get_height() // 2
                )
            )

    def render(self, screen):
        screen.fill((26, 30, 38))

        title_surface = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surface,
            (
                self.width // 2
                - title_surface.get_width() // 2,
                25
            )
        )

        score_surface = self.font_msg.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surface,
            (
                self.width // 2
                - score_surface.get_width() // 2,
                70
            )
        )

        timer_color = (
            (240, 80, 80)
            if self.time_left <= 5
            else (255, 220, 80)
        )

        timer_surface = self.font_msg.render(
            f"Time: {self.time_left}",
            True,
            timer_color
        )

        screen.blit(
            timer_surface,
            (
                self.width // 2
                - timer_surface.get_width() // 2,
                100
            )
        )

        self.render_tiles(screen)

        hint_display = " ".join(
            letter if revealed else "_"
            for letter, revealed in zip(
                self.secret_word,
                self.revealed_letters
            )
        )

        hint_surface = self.font_msg.render(
            hint_display,
            True,
            (255, 220, 80)
        )

        screen.blit(
            hint_surface,
            (
                self.width // 2
                - hint_surface.get_width() // 2,
                220
            )
        )

        self.input_box.render(screen)

        pygame.draw.rect(
            screen,
            (50, 150, 85),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        submit_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            submit_text,
            (
                self.submit_btn.centerx
                - submit_text.get_width() // 2,
                self.submit_btn.centery
                - submit_text.get_height() // 2
            )
        )

        pygame.draw.rect(
            screen,
            (180, 120, 45),
            self.hint_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.hint_btn,
            width=2,
            border_radius=6
        )

        hint_text = self.font_btn.render(
            "HINT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_text,
            (
                self.hint_btn.centerx
                - hint_text.get_width() // 2,
                self.hint_btn.centery
                - hint_text.get_height() // 2
            )
        )

        feedback_surface = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surface,
            (
                self.width // 2
                - feedback_surface.get_width() // 2,
                315
            )
        )