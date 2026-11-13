# Error404
## PORCENTAGEM : 85%

1. Título do Jogo -
Error 404: Diploma not found

2. Descrição Geral -
Jogo rítmico inspirado em Friday Night Funkin, ambientado no IFRN Campus Caicó, especialmente nos laboratórios de informática. A proposta é que o jogador enfrente professores em batalhas musicais para conseguir se formar no curso. O jogo possui 3 fases, cada uma com seu professor (ou dupla de professores), música, cenário e ranking de pontuação.

3. Objetivo do Jogo -
O jogador deve vencer professores em batalhas musicais, acumulando pontos e mantendo a barra de vida em cada fase para, ao final, conquistar seu diploma. Ao terminar cada fase, o desempenho recebe uma classificação (Perfeito, Ótimo, Bom, Regular ou Ruim) e a pontuação entra no ranking da fase.

4. Personagem Principal -
O personagem principal é um aluno do IFRN. Ele reage às ações do jogador durante as batalhas rítmicas, com um sprite para cada seta (↑ ↓ ← →), um para quando o jogador erra e um parado. Sua "vida" é representada pela barra de vida. Antes de começar, o jogador digita o próprio nome (até 12 caracteres), que é utilizado no ranking.

5. Inimigos e Obstáculos -
Os inimigos são os professores (Joaildo, Hugo e Max, Romerito), que ficam no lado direito da tela e executam os movimentos de cada seta quando ela chega ao receptor, como se estivessem "cantando" a sequência. A parte roxa da barra de vida representa o professor: quanto mais o jogador erra, mais a barra se enche de roxo. Nas fases com dois professores, um fica à frente e outro mais ao fundo. Não há sistema de colisão, pois o foco do jogo é o ritmo.

6. Cenário (Mapa) -
O jogo se passa nos laboratórios no IFRN Campus-Caicó, com o pátio, laboratorio de informática e a pista de atletismo. Cada fase tem seu próprio fundo. O objetivo final é vencer todos os professores para alcançar a formatura.

7. Sistema de Pontuação -
O jogador deve acertar a direção das setas que representam notas musicais, apertando a tecla quando a seta passa pelo receptor. Cada acerto concede pontos de acordo com a precisão: perfeito (350), bom (200), ruim (50) e errou (0). O feedback ("Perfeito!", "Bom!", "É...", "Errou!") aparece na tela e cada acerto recupera a barra de vida. Ao fim da fase, a nota final é calculada pela proporção entre os pontos feitos e o máximo possível. Os resultados são gravados em arquivo e exibidos na tela de Ranking, com as 10 melhores pontuações por fase (uma por jogador).

8. Sistema de Vida -
A barra de vida é única e compartilhada com o professor, e inicia equilibrada em 50%. Acertar uma seta recupera a barra; apertar uma tecla sem ter seta para acertar tira ou errar baixa a vida. Quanto menos barra do jogador, mais barra do professor. Se a barra do jogador chegar a zero, ele perde a fase.

9. Controles -
Setas (← ↑ → ↓) → Executar as notas musicais/navegar nos menus e na seleção de fase
Enter → Selecionar opções/confirmar nome/continuar nas telas de vitória e derrota
Esc → Voltar nas telas de menu, cancelar a contagem inicial ou, durante a fase, pausar e abrir a confirmação para sair da fase

10. Fluxo do Jogo -
O jogo inicia com a tela de logo e a digitação do nome do jogador, seguindo para o menu principal (Começar, Score, Créditos e Sair). Em "Começar", o jogador escolhe a fase e, após uma contagem regressiva (3, 2, 1, VAI!), enfrenta o professor. Durante a batalha, deve acertar o maior número possível de setas. Ao final, aparece a tela de vitória (com pontos e classificação) ou de derrota, e o jogador retorna à seleção de fase. A vitória ocorre ao ficar com vida até o final da música da fase; a derrota acontece quando o jogador zerar a barra de vida. Vencer uma fase desbloqueia a próxima.

11. Regras do Jogo -
O jogador deve se manter com vida até o fim da fase. Caso perca, deverá reiniciar a fase desde o início. As fases são desbloqueadas em sequência e só a pontuação de fases vencidas é registrada no ranking.

12. Estrutura do Projeto -

• Organização dos arquivos do jogo:

/Assets → Pasta de Assets geral do jogo

    ↪︎ /Arquivos_txt → Arquivos que guardam informações como sequencias das setas (fase1.txt, fase2.txt, fase3.txt) e ranking (ranking.txt)

    ↪︎ /Fontes → Fontes utilizadas 

    ↪︎ /Music → Trilhas sonoras das fases e do menu, músicas de vitória/derrota e efeito da contagem

    ↪︎ /Sprites → Imagens dos sprites dos personagens (aluno e professores) e setas

    ↪︎ /Telas → Telas (logo, menu, créditos, fundos das fases)

/Class → Lógica do jogo (ritmo, pontuação, mecânicas...)

    ↪︎ seta.py, pontuacao.py, barra_vida.py, fase.py, sinc.py, ranking.py, intro.py, tela_inicial.py, tela_fim.py

jogo.py → Classe principal que controla o loop, os estados e a ligação entre todas as partes

• Separação por responsabilidades:

Player (Aluno) → Entrada do jogador (teclas) e execução das notas, com sprites de reação

Professores (Inimigos) → Sprites que reagem às setas de cada fase

Sistema de Ritmo → Sincronização música + inputs

Mapa/Cenário → Ambientação visual (fundos de cada fase)

Sistema Geral (Game Manager) → Controle de fases, progresso e vitória/derrota

Interface (UI) → Menu, seleção de fase, barra de vida, feedback de acerto, telas de vitória/derrota, ranking e créditos

Sistema de Áudio → Reprodução e sincronização sonora, feitas com o pygame.mixer

13. Funcionalidades Mínimas -
O jogo deve conter:
Músicas sincronizadas com as setas ✔ (implementado, com as notas de cada fase em arquivo .txt)
Sistema de vida funcional ✔ (implementado)
Controles responsivos ✔ (implementado)
Pelo menos um professor, um personagem jogável e um cenário representando o IFRN ✔ (implementado: 3 fases, 4 professores, 1 personagem jogável e 3 cenários)

Andamento: todas as funcionalidades mínimas estão concluídas, além de extras que não estavam no escopo inicial (entrada de nome, ranking por fase, classificação final, telas de vitória/derrota, pausa com confirmação de saída, créditos e contagem regressiva).

14. Melhorias Futuras -
Pontos que ainda faltam na implementação:

Tela/cena final de formatura (diploma) ao vencer a última fase
Acionar Sprites do personagem principal e do professor na barra de vida se movendo junto com ela
Melhorar o visual da tela de seleção de fase

Melhorias futuras:

Adição de novas fases e professores
Exploração livre do campus
Seleção de dificuldade
Modo livre (escolha de músicas e fases)