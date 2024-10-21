import cv2
import mediapipe as mp
import pygame

class Camera:
    def __init__(self):
        """Configura a câmera e a detecção de mãos usando MediaPipe."""
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Reduzir resolução da câmera
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)  # Detectar apenas uma mão
        self.mp_draw = mp.solutions.drawing_utils

    def detect_gesture(self, hand_landmarks):
        """Detecta o gesto da mão baseado nas posições dos dedos, verificando todos os dedos."""
        thumb_tip = hand_landmarks.landmark[4].y
        index_tip = hand_landmarks.landmark[8].y
        middle_tip = hand_landmarks.landmark[12].y
        ring_tip = hand_landmarks.landmark[16].y

        # Verificar gesto de pedra (todos os dedos dobrados)  
        if index_tip < thumb_tip and middle_tip < thumb_tip:
            return 'pedra'
        # Verificar gesto de tesoura (somente polegar, indicador e médio levantados)  
        elif index_tip > thumb_tip and middle_tip > thumb_tip and ring_tip < thumb_tip:
            return 'tesoura'
        # Verificar gesto de papel (todos os dedos esticados)  
        elif index_tip > thumb_tip and middle_tip > thumb_tip and ring_tip > thumb_tip:
            return 'papel'
        return None


    def get_frame(self):
        """Captura um frame da câmera, processa para detectar mãos e retorna o gesto."""
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Corrigindo cores (BGR para RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processar a imagem com MediaPipe para detectar a mão
        results = self.hands.process(frame_rgb)
        player_move = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                player_move = self.detect_gesture(hand_landmarks)

        # Redimensionar o frame
        frame_resized = cv2.resize(frame_rgb, (300, 300))
        frame_surface = pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")

        return player_move, frame_surface

    def release(self):
        """Libera os recursos da câmera."""
        self.cap.release()
