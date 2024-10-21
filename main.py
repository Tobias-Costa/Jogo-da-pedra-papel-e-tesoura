import pygame
from camera import Camera
from game_logic import GameLogic
from display import Display

# Configurações iniciais
pygame.init()
screen_width, screen_height = 1280, 720  # Ajustado para tela 1280x720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pedra, Papel ou Tesoura")

# Inicializando componentes
camera = Camera()
game_logic = GameLogic()
display = Display(screen)

# Controlador de framerate
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    screen.fill((0, 0, 0))  # Limpar a tela a cada frame

    # Eventos de saída e reinício
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Exibir tela de fim de jogo
        if game_logic.game_over:
            if game_logic.player_score > game_logic.computer_score:
                display.display_end_screen("assets/vitoria_background.jpg", "Parabéns! Você ganhou!")
            else:
                display.display_end_screen("assets/derrota_background.jpg", "Você perdeu! Tente novamente.")
            # Reiniciar o jogo após a exibição
            game_logic.reset_game()

    # Capturar a imagem da câmera e detectar a jogada do jogador
    player_move, frame_surface = camera.get_frame()

    # Lógica do jogo e atualização do placar se não estiver entre rodadas
    current_time = pygame.time.get_ticks()
    if player_move:
        game_logic.update(player_move, current_time)

    # Exibir a imagem da câmera, ícones e placar na tela
    display.update_display(frame_surface, game_logic)

    # Atualizar tela
    pygame.display.flip()

    # Limitar o framerate
    clock.tick(30)

# Finalizar
camera.release()
pygame.quit()
