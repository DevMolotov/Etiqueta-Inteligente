import time
from google import genai
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

# ==========================================
# CONFIGURAÇÕES DE HARDWARE (OLED)
# ==========================================
# Inicia a comunicação I2C na porta 1, com o endereço do OLED
serial = i2c(port=1, address=0x3C)

# Define o modelo do OLED (ssd1306 é o chip de 99% desses displays de 0.96")
device = ssd1306(serial)

# Carrega uma fonte padrão para desenhar as letras
# No futuro, você pode baixar arquivos .ttf e carregar fontes customizadas!
fonte_padrao = ImageFont.load_default()

# ==========================================
# CONFIGURAÇÕES DA IA (GEMINI)
# ==========================================
MINHA_CHAVE_API = "Insira a chave da API aqui(de preferência use a do Gemini)" 
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

def exibir_texto_oled(linha1, linha2=""):
    """Função auxiliar para desenhar textos na tela OLED"""
    with canvas(device) as draw:
        # draw.text((x, y), texto, cor, fonte)
        draw.text((0, 0), linha1, fill="white", font=fonte_padrao)
        if linha2:
            draw.text((0, 16), linha2, fill="white", font=fonte_padrao)

# ==========================================
# LOOP PRINCIPAL DO SISTEMA
# ==========================================
try:
    print("Sistema OLED iniciado. Pressione CTRL+C para encerrar.")
    
    while True:
        exibir_texto_oled("Aguardando", "Cliente...")
        time.sleep(3)

        cliente_atual = "Matheus, 22 anos, estudante de engenharia, cliente Ouro."
        print(f"\nAnalisando: {cliente_atual}")
        
        exibir_texto_oled("Avaliando", "Perfil (IA)...")
        
        preco_final = calcular_preco_gemini(cliente_atual)
        print(f"Preço: R$ {preco_final:.2f}")
        
        # Exibe o resultado final
        exibir_texto_oled("Preco Exclusivo:", f"R$ {preco_final:.2f}")
        
        time.sleep(10)

except KeyboardInterrupt:
    # Limpa a tela ao sair
    device.clear()
    print("\nSistema encerrado.")
