import pygame, sys, time, random

dificuldades = {
    'Fácil': 10,
    'Médio': 25,
    'Difícil': 40,
    'Mais Difícil': 60,
    'Impossível': 120
}

largura_janela = 720
altura_janela = 480

class Cobra:
    def __init__(self):
        self.posicao = [100, 50]
        self.corpo = [[100, 50], [90, 50], [80, 50]]
        self.direcao = 'DIREITA'
        self.mudanca_para = self.direcao

    def mudar_direcao(self, direcao):
        if direcao == 'CIMA' and self.direcao != 'BAIXO':
            self.direcao = 'CIMA'
        if direcao == 'BAIXO' and self.direcao != 'CIMA':
            self.direcao = 'BAIXO'
        if direcao == 'ESQUERDA' and self.direcao != 'DIREITA':
            self.direcao = 'ESQUERDA'
        if direcao == 'DIREITA' and self.direcao != 'ESQUERDA':
            self.direcao = 'DIREITA'

    def mover(self, posicao_comida):
        if self.direcao == 'CIMA':
            self.posicao[1] -= 10
        if self.direcao == 'BAIXO':
            self.posicao[1] += 10
        if self.direcao == 'ESQUERDA':
            self.posicao[0] -= 10
        if self.direcao == 'DIREITA':
            self.posicao[0] += 10

        self.corpo.insert(0, list(self.posicao))
        if self.posicao[0] != posicao_comida[0] or self.posicao[1] != posicao_comida[1]:
            self.corpo.pop()
        else:
            return True
        return False

    def verificar_colisao(self):
        if self.posicao[0] < 0 or self.posicao[0] > largura_janela - 10:
            return True
        if self.posicao[1] < 0 or self.posicao[1] > altura_janela - 10:
            return True
        for bloco in self.corpo[1:]:
            if self.posicao[0] == bloco[0] and self.posicao[1] == bloco[1]:
                return True
        return False

class JogoCobra:
    def __init__(self):
        self.cobra = Cobra()
        self.pontuacao = 0
        self.dificuldade = 25
        self.posicao_comida = [random.randrange(1, (largura_janela // 10)) * 10, random.randrange(1, (altura_janela // 10)) * 10]
        self.comida_spawn = True
        self.janela_jogo = pygame.display.set_mode((largura_janela, altura_janela))
        pygame.display.set_caption('Jogo da Cobra')
        self.controlador_fps = pygame.time.Clock()

    def escolher_dificuldade(self):
        while True:
            self.janela_jogo.fill(preto)
            fonte = pygame.font.SysFont('times new roman', 30)
            superficie_titulo = fonte.render('Escolha a Dificuldade:', True, branco)
            self.janela_jogo.blit(superficie_titulo, (largura_janela / 4, altura_janela / 6))

            dificuldades_texto = [
                '1. Fácil',
                '2. Médio',
                '3. Difícil',
                '4. Mais Difícil',
                '5. Impossível'
            ]

            for idx, texto in enumerate(dificuldades_texto):
                superficie_opcao = fonte.render(texto, True, branco)
                self.janela_jogo.blit(superficie_opcao, (largura_janela / 4, altura_janela / 3 + idx * 40))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.dificuldade = dificuldades['Fácil']
                        return
                    elif evento.key == pygame.K_2:
                        self.dificuldade = dificuldades['Médio']
                        return
                    elif evento.key == pygame.K_3:
                        self.dificuldade = dificuldades['Difícil']
                        return
                    elif evento.key == pygame.K_4:
                        self.dificuldade = dificuldades['Mais Difícil']
                        return
                    elif evento.key == pygame.K_5:
                        self.dificuldade = dificuldades['Impossível']
                        return

    def fim_de_jogo(self):
        while True:
            self.janela_jogo.fill(preto)
            fonte = pygame.font.SysFont('times new roman', 90)
            superficie_fim = fonte.render('SE FODEU!', True, vermelho)
            retangulo_fim = superficie_fim.get_rect()
            retangulo_fim.midtop = (largura_janela / 2, altura_janela / 4)
            self.janela_jogo.blit(superficie_fim, retangulo_fim)
            self.mostrar_pontuacao(0, vermelho, 'times', 20)

            fonte_opcao = pygame.font.SysFont('times new roman', 30)
            superficie_reiniciar = fonte_opcao.render('Pressione R para Reiniciar ou Q para Sair', True, branco)
            retangulo_reiniciar = superficie_reiniciar.get_rect()
            retangulo_reiniciar.midtop = (largura_janela / 2, altura_janela / 1.5)
            self.janela_jogo.blit(superficie_reiniciar, retangulo_reiniciar)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.__init__()
                        self.escolher_dificuldade()
                        self.jogar()
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def mostrar_pontuacao(self, escolha, cor, fonte, tamanho):
        fonte_pontuacao = pygame.font.SysFont(fonte, tamanho)
        superficie_pontuacao = fonte_pontuacao.render('Pontuação: ' + str(self.pontuacao), True, cor)
        retangulo_pontuacao = superficie_pontuacao.get_rect()
        if escolha == 1:
            retangulo_pontuacao.midtop = (largura_janela / 10, 15)
        else:
            retangulo_pontuacao.midtop = (largura_janela / 2, altura_janela / 1.25)
        self.janela_jogo.blit(superficie_pontuacao, retangulo_pontuacao)

    def jogar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP or evento.key == ord('w'):
                        self.cobra.mudanca_para = 'CIMA'
                    if evento.key == pygame.K_DOWN or evento.key == ord('s'):
                        self.cobra.mudanca_para = 'BAIXO'
                    if evento.key == pygame.K_LEFT or evento.key == ord('a'):
                        self.cobra.mudanca_para = 'ESQUERDA'
                    if evento.key == pygame.K_RIGHT or evento.key == ord('d'):
                        self.cobra.mudanca_para = 'DIREITA'
                    if evento.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            self.cobra.mudar_direcao(self.cobra.mudanca_para)
            comeu_comida = self.cobra.mover(self.posicao_comida)
            if comeu_comida:
                self.pontuacao += 1
                self.posicao_comida = [random.randrange(1, (largura_janela // 10)) * 10, random.randrange(1, (altura_janela // 10)) * 10]

            self.janela_jogo.fill(preto)
            for pos in self.cobra.corpo:
                pygame.draw.rect(self.janela_jogo, verde, pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(self.janela_jogo, branco, pygame.Rect(self.posicao_comida[0], self.posicao_comida[1], 10, 10))

            if self.cobra.verificar_colisao():
                self.fim_de_jogo()

            self.mostrar_pontuacao(1, branco, '', 20)

            pygame.display.update()

            self.controlador_fps.tick(self.dificuldade)

if __name__ == "__main__":
    pygame.init()
    preto = pygame.Color(0, 0, 0)
    branco = pygame.Color(255, 255, 255)
    vermelho = pygame.Color(255, 0, 0)
    verde = pygame.Color(0, 255, 0)

    jogo = JogoCobra()
    jogo.escolher_dificuldade()
    jogo.jogar()
