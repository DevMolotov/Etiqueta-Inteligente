# Smart Pricing: Precificação Dinâmica com IA

Este projeto transforma um **Raspberry Pi** em um sistema inteligente de balcão. Ele utiliza a nova API oficial do **Google Gemini (`google-genai`)** para analisar o perfil de um cliente em tempo real e calcular um preço exclusivo e personalizado, aplicando regras de negócio de forma lógica e autônoma. O valor final e as interações visuais são exibidos em um **Display Gráfico OLED I2C (0.96")**.

## Hardware Necessário

* 1x Raspberry Pi (Recomendado Pi 3 ou Pi 4)
* 1x Display OLED 0.96" I2C (Controlador SSD1306)
* 4x Cabos Jumper Fêmea-Fêmea
* Fonte de alimentação (5V/3A) para o Raspberry Pi

## Esquema de Ligação (Pinout I2C)

A comunicação com a tela utiliza o barramento I2C. 
> **ATENÇÃO:** Diferente dos displays LCD antigos que usavam 5V, a grande maioria dos displays OLED de 0.96" opera em **3.3V**. Ligar o VCC do OLED no pino de 5V do Raspberry Pi pode queimar a tela instantaneamente.

| Pino no OLED I2C | Pino no Raspberry Pi (Físico) | Função |
| :--- | :--- | :--- |
| **GND** | Pino 6 | Terra (Ground) |
| **VCC** | **Pino 1 ou 17** | Alimentação (**3.3V**) |
| **SDA** | Pino 3 (GPIO 2) | Dados |
| **SCL** | Pino 5 (GPIO 3) | Clock |

## Configuração do Sistema (Raspberry Pi OS)

### 1. Habilitar o I2C no Sistema
Antes de rodar o código, a porta I2C deve estar ativada:
1. No terminal, rode: `sudo raspi-config`
2. Vá em **Interface Options** > **I2C** e selecione **Yes**.
3. Reinicie o sistema: `sudo reboot`.
4. *(Opcional)* Para verificar a comunicação, instale o `i2c-tools` e rode `i2cdetect -y 1`. O endereço padrão para telas OLED é o **`0x3C`**.

### 2. Preparar o Ambiente Python
Recomenda-se o uso de um ambiente virtual (`venv`) para evitar conflitos com o sistema operacional.
```bash
# Crie o ambiente virtual na pasta do projeto
python3 -m venv venv

# Ative o ambiente
source venv/bin/activate
