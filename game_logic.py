import random

class GameLogic:
    def __init__(self):
        """Inicializa o jogo, define placares e estado de jogo."""
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_over = False
        self.computer_choice = None
        self.round_timer = 0  # Temporizador para controlar o tempo entre rodadas
        self.round_delay = 2000  # 2 segundos de intervalo entre rodadas

    def computer_move(self):
        """Escolha aleatória do movimento da máquina."""
        return random.choice(['pedra', 'papel', 'tesoura'])

    def determine_winner(self, player, computer):
        """Determina o vencedor da rodada com base nos movimentos."""
        if player == computer:
            return 'Empate'
        elif (player == 'pedra' and computer == 'tesoura') or \
             (player == 'papel' and computer == 'pedra') or \
             (player == 'tesoura' and computer == 'papel'):
            return 'Jogador'
        else:
            return 'Computador'

    def update(self, player_move, current_time):
        """Atualiza o estado do jogo após uma jogada."""
        if not self.game_over and current_time - self.round_timer >= self.round_delay:
            self.computer_choice = self.computer_move()
            winner = self.determine_winner(player_move, self.computer_choice)

            if winner == 'Jogador':
                self.player_score += 1
            elif winner == 'Computador':
                self.computer_score += 1

            self.rounds_played += 1
            self.round_timer = current_time  # Reiniciar o temporizador para o próximo round

            if self.rounds_played >= 3:
                self.game_over = True

    def reset_game(self):
        """Reinicia as variáveis do jogo para começar uma nova partida."""
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_over = False
        self.computer_choice = None
        self.round_timer = 0
