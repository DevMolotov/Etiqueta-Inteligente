from RPLCD.i2c import CharLCD
import time

# Configuração do LCD no endereço padrão 0x27
lcd = CharLCD('PCF8574', 0x27)

def prever_preco_com_ia(dados_cliente):
    # Aqui entraria o seu modelo de Machine Learning (ex: scikit-learn)
    # ou a chamada para a API do Gemini.
    # Por enquanto, retornamos um valor fixo simulado.
    print(f"Analisando perfil: {dados_cliente}")
    time.sleep(2) # Simulando o tempo de processamento da IA
    return 85.50

# Loop principal
try:
    lcd.clear()
    lcd.write_string('Aguardando\r\nCliente...')
    time.sleep(3)

    # Simulação de um cliente chegando (ex: leu um cartão RFID)
    perfil_cliente = {"idade": 22, "estudante": True, "fidelidade": "alta"}
    
    lcd.clear()
    lcd.write_string('Analisando...')
    
    preco = prever_preco_com_ia(perfil_cliente)
    
    lcd.clear()
    lcd.write_string('Preco Exclusivo:\r\n')
    lcd.write_string(f'R$ {preco:.2f}')
    
    time.sleep(10)

except KeyboardInterrupt:
    lcd.clear()
    print("Sistema encerrado.")
