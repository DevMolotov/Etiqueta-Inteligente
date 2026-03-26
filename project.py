import time
from google import genai
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

# CONFIGURAÇÕES DE HARDWARE (OLED)
try:
    # Inicia a comunicação I2C na porta 1, com o endereço do OLED (0x3C)
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
except Exception as e:
    print(f"Erro ao conectar o OLED. Verifique os fios SDA/SCL e VCC em 3.3V: {e}")
    exit()
    
# CONFIGURAÇÕES ESTÉTICAS (FONTES & LAYOUT)
try:
    font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_path_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    fonte_titulo = ImageFont.truetype(font_path_bold, 14)
    fonte_preco = ImageFont.truetype(font_path_bold, 24)
    fonte_padrao = ImageFont.truetype(font_path_regular, 10)
except:
    print("Aviso: Fontes premium não encontradas. Usando fonte padrão.")
    fonte_titulo = fonte_preco = fonte_padrao = ImageFont.load_default()

def centralizar_texto(draw_obj, texto, fonte, altura_y):
    """Calcula a posição X para centralizar o texto perfeitamente na tela"""
    left, top, right, bottom = draw_obj.textbbox((0, 0), texto, font=fonte)
    largura_texto = right - left
    posicao_x = (device.width - largura_texto) // 2
    draw_obj.text((posicao_x, altura_y), texto, fill="white", font=fonte)

# CONFIGURAÇÕES DA IA (GEMINI)
MINHA_CHAVE_API = "Insira sua chave aqui" 
client = genai.Client(api_key=MINHA_CHAVE_API)

def calcular_preco_gemini(perfil_cliente):
    preco_base = 100.00
    
    prompt = f"""
    Você é o gerente de vendas de uma loja. O preço base é R$ {preco_base}.
    Avalie o perfil deste cliente e aplique descontos lógicos.
    Perfil: {perfil_cliente}
    
    Responda APENAS com o número final usando ponto. Nada mais.
    """
    
    try:
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return float(resposta.text.strip())
    except Exception as e:
        print(f"Erro na IA: {e}")
        return preco_base

# FUNÇÕES VISUAIS & ANIMAÇÕES (OLED)
def exibir_tela_espera():
    """Desenha a tela de aguardando"""
    with canvas(device) as draw:
        centralizar_texto(draw, "Aguardando", fonte_titulo, 15)
        centralizar_texto(draw, "Cliente...", fonte_titulo, 35)

def exibir_preco_estetico(preco):
    """Desenha o preço final centralizado e em destaque"""
    texto_preco = f"R$ {preco:.2f}"
    with canvas(device) as draw:
        centralizar_texto(draw, "Preco Exclusivo:", fonte_padrao, 5)
        centralizar_texto(draw, texto_preco, fonte_preco, 25)

def desenhar_rosto_dancando(draw, tilt, texto_placeholder="CLIENTE"):
    """Desenha os frames da dancinha"""
    centro_x = device.width // 2
    rosto_x = centro_x + (tilt * 10) # Movimenta o rosto para os lados
    rosto_y = 25
    raio = 20
    
    # Cabeça
    draw.ellipse((rosto_x - raio, rosto_y - raio, rosto_x + raio, rosto_y + raio), outline="white")
    # Olhos
    draw.ellipse((rosto_x - 8 - 2, rosto_y - 5 - 2, rosto_x - 8 + 2, rosto_y - 5 + 2), fill="white")
    draw.ellipse((rosto_x + 8 - 2, rosto_y - 5 - 2, rosto_x + 8 + 2, rosto_y - 5 + 2), fill="white")
    # Sorriso feliz
    draw.arc((rosto_x - 8, rosto_y + 5, rosto_x + 8, rosto_y + 10), start=0, end=180, fill="white")
    # Placeholder em baixo
    centralizar_texto(draw, texto_placeholder, fonte_padrao, device.height - 12)

def rodar_dancinha_placeholder(duracao=5):
    """Loop de frames para simular a animação no OLED"""
    tempo_inicio = time.time()
    poses = [-1, 0, 1, 0] # Esquerda, Centro, Direita, Centro
    frame_atual = 0
    
    while (time.time() - tempo_inicio) < duracao:
        with canvas(device) as draw:
            desenhar_rosto_dancando(draw, poses[frame_atual])
        
        time.sleep(0.15) # Velocidade da dança
        frame_atual = (frame_atual + 1) % len(poses)

# LOOP PRINCIPAL DO SISTEMA
try:
    print("Sistema OLED iniciado. Pressione CTRL+C para encerrar.")
    
    while True:
        # 1. Aguardando Cliente
        exibir_tela_espera()
        time.sleep(3)

        # 2. Avaliação da IA
        cliente_atual = "Matheus, 22 anos, estudante de engenharia, cliente Ouro."
        print(f"\nAnalisando: {cliente_atual}")
        
        with canvas(device) as draw:
            centralizar_texto(draw, "Avaliando", fonte_titulo, 15)
            centralizar_texto(draw, "Perfil (IA)...", fonte_padrao, 40)
            
        preco_final = calcular_preco_gemini(cliente_atual)
        print(f"Preço: R$ {preco_final:.2f}")
        
        # 3. Exibe o preço centralizado
        exibir_preco_estetico(preco_final)
        
        # Simula tempo de decisão do cliente
        time.sleep(4) 
        
        # 4. Confirmação de Venda e Animação
        print("Venda realizada! Iniciando comemoração...")
        with canvas(device) as draw:
            centralizar_texto(draw, "VENDIDO!", fonte_preco, 20)
        time.sleep(1.5)
        
        # Roda a dancinha por 5 segundos
        rodar_dancinha_placeholder(duracao=5)
        
        # Limpa para o próximo ciclo
        device.clear()
        time.sleep(1)

except KeyboardInterrupt:
    device.clear()
    print("\nSistema encerrado.")
