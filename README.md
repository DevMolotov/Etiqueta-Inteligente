# 🏷️ Sistema de Precificação Dinâmica com IA (Raspberry Pi)

Este projeto é um protótipo de sistema embarcado em um **Raspberry Pi** que avalia o perfil de um cliente e gera um preço personalizado dinamicamente. O resultado (valor final) é exibido em tempo real em um **Display LCD 16x2 via interface I2C**.

Atualmente, o código simula o tempo de processamento e a lógica de uma Inteligência Artificial, servindo como base estrutural para a futura integração com modelos de Machine Learning (como `scikit-learn`) ou APIs externas (como Google Gemini).

## 🛠️ Hardware Necessário

* 1x Raspberry Pi (Modelo 3 ou 4 recomendado)
* 1x Display LCD 16x2
* 1x Módulo I2C para Display LCD (Geralmente soldado ao display)
* 4x Cabos Jumper Fêmea-Fêmea
* Fonte de alimentação adequada para o Raspberry Pi

## 🔌 Esquema de Ligação (Pinout)

A comunicação entre o Raspberry Pi e o display é feita através do barramento I2C. Conecte os pinos da seguinte forma:

| Pino no LCD I2C | Pino no Raspberry Pi (Físico) | Função |
| :--- | :--- | :--- |
| **GND** | Pino 6 | Terra (Ground) |
| **VCC** | Pino 2 ou 4 | Alimentação (5V) |
| **SDA** | Pino 3 (GPIO 2) | Dados (Serial Data) |
| **SCL** | Pino 5 (GPIO 3) | Clock (Serial Clock) |

> **Atenção:** A maioria dos displays 16x2 exige 5V no VCC para que a luz de fundo (backlight) funcione corretamente com bom contraste.

## ⚙️ Configuração do Ambiente

### 1. Habilitar a interface I2C no Raspberry Pi
Antes de rodar o código, é obrigatório ativar o I2C no sistema operacional do Raspberry Pi:
1. Abra o terminal e digite: `sudo raspi-config`
2. Navegue até **Interface Options** > **I2C**.
3. Selecione **Yes** para habilitar e reinicie o Raspberry Pi.

### 2. Instalar as Dependências (Python)
O projeto utiliza a biblioteca `RPLCD` para facilitar a comunicação com o display. Instale-a via `pip`:

```bash
pip install RPLCD smbus2
