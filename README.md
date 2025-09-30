# 🍄 Super Mario Bros - Python Implementation

Uma implementação completa do clássico Super Mario Bros em Python usando Pygame, com múltiplas fases e mecânicas autênticas do jogo original.

## ✨ Características

### 🎮 Jogabilidade
- Mecânicas clássicas do Mario (pular, correr, power-ups)
- Sistema de física realista com gravidade e colisões
- Múltiplas fases com designs únicos:
  - **Fase 1**: Clássica fase overworld
  - **Fase 2**: Tema subterrâneo com novos desafios

### 🎯 Elementos do Jogo
- **Inimigos**: Goombas, Koopa Troopas com IA autêntica
- **Power-ups**: Super Mushroom, Fire Flower
- **Obstáculos**: Pipes, blocos de tijolo, caixas de moeda
- **Sistema de pontuação** completo
- **Checkpoint system** para salvar progresso

### 🎵 Áudio e Visual
- Gráficos pixel-perfect fiéis ao original
- Trilha sonora e efeitos sonoros autênticos
- Animações suaves e responsivas
- Interface de usuário intuitiva

## 🛠️ Requisitos Técnicos

- **Python**: 3.8 ou superior
- **Pygame**: Para renderização e áudio
- **PIL (Pillow)**: Para processamento de imagens
- **Sistema Operacional**: Windows, macOS, Linux

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd Mario-Level-1
```

### 2. Configure o ambiente virtual
```bash
# Usando uv (recomendado)
uv venv .venvMarioDoArmario
source .venvMarioDoArmario/bin/activate  # Linux/macOS
# ou
.venvMarioDoArmario\Scripts\activate     # Windows

# Ou usando venv tradicional
python -m venv .venvMarioDoArmario
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## 🚀 Como Jogar

### Iniciar o jogo
```bash
# Jogo completo com menu
python data/main.py

# Iniciar diretamente na Fase 1
python mario_level_1.py

# Iniciar diretamente na Fase 2
python start_level2_direct.py

# Seletor de fases
python mario_level_selector.py
```

### 🎮 Controles
| Tecla | Ação |
|-------|------|
| ⬅️ ➡️ | Mover Mario |
| ⬆️ | Pular |
| ⬇️ | Agachar / Entrar em pipes |
| **Space** | Pular (alternativo) |
| **Enter** | Iniciar jogo / Pausar |
| **ESC** | Menu principal |

### 🏆 Sistema de Pontuação
- **Goomba**: 100 pontos
- **Koopa Troopa**: 200 pontos
- **Moedas**: 50 pontos cada
- **Power-ups**: 1000 pontos
- **Blocos quebrados**: 50 pontos

## 📁 Estrutura do Projeto

```
Mario-Level-1/
├── 📂 data/                    # Código principal do jogo
│   ├── 📂 components/          # Componentes do jogo
│   │   ├── mario.py           # Classe principal do Mario
│   │   ├── enemies.py         # Inimigos (Goomba, Koopa)
│   │   ├── powerups.py        # Power-ups e itens
│   │   ├── collider.py        # Sistema de colisões
│   │   └── ...
│   ├── 📂 states/             # Estados do jogo
│   │   ├── main_menu.py       # Menu principal
│   │   ├── level1.py          # Fase 1
│   │   ├── level2.py          # Fase 2 (subterrânea)
│   │   └── ...
│   ├── main.py                # Ponto de entrada principal
│   ├── setup.py               # Configurações e recursos
│   └── constants.py           # Constantes do jogo
├── 📂 resources/              # Assets do jogo
│   ├── 📂 graphics/           # Sprites e backgrounds
│   ├── 📂 music/              # Trilha sonora
│   └── 📂 sound/              # Efeitos sonoros
├── 📂 logs/                   # Logs de debug
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🔧 Desenvolvimento

### 🐛 Debug e Logs
O jogo gera logs detalhados para debug:
- Logs são salvos em `logs/mario_game_YYYYMMDD_HHMMSS.log`
- Logs de debug específicos em `mario_debug_*.log`
- Configure o nível de log em `data/logging_config.py`

### 🧪 Testes
```bash
# Testar transição entre fases
python test_level_transition.py

# Testar Fase 2 especificamente
python test_level2.py
```

### 🎨 Criação de Assets
- Backgrounds são criados programaticamente usando PIL
- Sprites originais em formato PNG
- Áudio em formatos OGG e WAV

## 🚧 Funcionalidades em Desenvolvimento

- [ ] Fase 3 (Castelo)
- [ ] Modo multiplayer
- [ ] Editor de fases
- [ ] Mais power-ups
- [ ] Sistema de vidas
- [ ] High scores online

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Padrões de Código

- Seguimos PEP 8 para estilo de código Python
- Comentários em inglês no código
- Commits em inglês
- Documentação em português (README)
- Sem uso de emojis no código

## 🐛 Problemas Conhecidos

- Performance pode variar em sistemas mais antigos
- Alguns efeitos sonoros podem ter delay em certas configurações
- Redimensionamento de janela não é suportado

## 📄 Licença

Este projeto é apenas para fins educacionais. Todos os assets gráficos e sonoros são propriedade da Nintendo.

## 🙏 Agradecimentos

- Nintendo pelo jogo original Super Mario Bros
- Comunidade Pygame pelos tutoriais e documentação
- Contribuidores do projeto

---

**Desenvolvido com ❤️ em Python**
