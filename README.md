# 🤖 Smart Pricing: Precificação Dinâmica com IA (Raspberry Pi + Google Gemini)

Este projeto transforma um **Raspberry Pi** em um sistema inteligente de balcão. Ele utiliza a API do **Google Gemini (Generative AI)** para analisar o perfil de um cliente em tempo real e calcular um preço exclusivo e personalizado, aplicando regras de negócio e descontos de forma lógica e autônoma. O valor final é exibido para o cliente em um **Display LCD 16x2 via interface I2C**.

## 🛠️ Hardware Necessário

* 1x Raspberry Pi (Recomendado Pi 3 ou Pi 4)
* 1x Display LCD 16x2
* 1x Módulo adaptador I2C para LCD
* 4x Cabos Jumper Fêmea-Fêmea
* Fonte de alimentação (5V/3A)

## 🔌 Esquema de Ligação (Pinout I2C)

A comunicação com a tela utiliza o barramento I2C. Conecte os pinos da seguinte maneira:

| Pino no Módulo I2C | Pino no Raspberry Pi (Físico) | Função |
| :--- | :--- | :--- |
| **GND** | Pino 6 | Terra (Ground) |
| **VCC** | Pino 2 ou 4 | Alimentação (5V obrigatório para o backlight) |
| **SDA** | Pino 3 (GPIO 2) | Dados |
| **SCL** | Pino 5 (GPIO 3) | Clock |

## ⚙️ Configuração Inicial (Raspberry Pi OS)

### 1. Habilitar o I2C no Sistema
Antes de rodar o código, a porta I2C deve estar ativada:
1. No terminal, rode: `sudo raspi-config`
2. Vá em **Interface Options** > **I2C** e selecione **Yes**.
3. Reinicie o sistema: `sudo reboot`.
4. *(Opcional)* Para verificar se a tela foi reconhecida e descobrir o endereço (ex: `0x27` ou `0x3F`), instale o `i2c-tools` e rode `i2cdetect -y 1`.

### 2. Preparar o Ambiente Python
Recomenda-se o uso de um ambiente virtual (venv) para evitar conflitos com o sistema operacional (especialmente no Raspberry Pi OS Bookworm ou superior).

```bash
# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente
source venv/bin/activate
