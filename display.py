import pygame

class Display:
    def __init__(self, screen):
        """Inicializa a tela onde o jogo será desenhado."""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 74)
        self.icon_pedra = pygame.image.load("assets/pedra.png")
        self.icon_papel = pygame.image.load("assets/papel.png")
        self.icon_tesoura = pygame.image.load("assets/tesoura.png")
        self.background_image = pygame.image.load("assets/tigre_arena.png")  # Carregar imagem de fundo
    
    def draw_background(self):
        """Desenha a imagem de fundo no jogo."""
        self.screen.blit(self.background_image, (0,0))

    def draw_score(self, player_score, computer_score):
        """Desenha o placar no topo da tela."""
        score_text = f"Jogador: {player_score}  |  Computador: {computer_score}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surface, (self.screen.get_width() // 2 - score_surface.get_width() // 2, 10))

    def draw_computer_choice(self, choice):
        """Desenha o ícone da escolha da máquina."""
        if choice == 'pedra':
            icon = self.icon_pedra
        elif choice == 'papel':
            icon = self.icon_papel
        else:
            icon = self.icon_tesoura

        # Centralizar o ícone à direita da tela
        icon_rect = icon.get_rect(center=(self.screen.get_width() * 3 // 4, self.screen.get_height() // 2))
        self.screen.blit(icon, icon_rect)

    def update_display(self, frame_surface, game_logic):
        """Atualiza a tela do jogo com a imagem da câmera, placar e escolha do computador."""
        # Desenhar fundo
        self.draw_background()

        # Desenhar a imagem da câmera
        if frame_surface:
            frame_rect = frame_surface.get_rect(center=(self.screen.get_width() // 4, self.screen.get_height() // 2))
            self.screen.blit(frame_surface, frame_rect)

        # Desenhar o placar
        self.draw_score(game_logic.player_score, game_logic.computer_score)

        # Desenhar a escolha da máquina
        if game_logic.computer_choice:
            self.draw_computer_choice(game_logic.computer_choice)

    def display_end_screen(self, background_image, message):
        """Exibe a tela de fim de jogo com mensagem personalizada."""
        # Carregar e desenhar imagem de fundo
        background = pygame.image.load(background_image)
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background, (0, 0))

        # Desenhar a mensagem no centro da tela
        text = self.large_font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Aguarda 3 segundos antes de reiniciar o jogo
