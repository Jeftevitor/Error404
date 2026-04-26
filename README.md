# Error404

1. Título do Jogo -
Error 404: Diploma not found

2. Descrição Geral -
Jogo rítmico inspirado em Friday Night Funkin, ambientado no IFRN Campus Caicó, especialmente nos laboratórios de informática. A proposta é que o jogador enfrente professores em batalhas musicais para conseguir se formar no curso.

3. Objetivo do Jogo -
O jogador deve vencer professores em batalhas musicais, acumulando nota suficiente em cada fase para, ao final, conquistar seu diploma.

4. Personagem Principal -
O personagem principal é um aluno do IFRN (podendo ser masculino ou feminino). Ele reage às ações do jogador durante as batalhas rítmicas. Sua “vida” é representada por uma nota, que deve ser maior ou igual a 60 para aprovação em cada disciplina.

5. Inimigos e Obstáculos -
Os inimigos são os professores, que tentam reduzir a nota do jogador durante as batalhas. Ambos executam movimentos baseados nas sequências rítmicas. Não há sistema de colisão, pois o foco do jogo é o ritmo.

6. Cenário (Mapa) -
O jogo se passa nos laboratórios de informática do IFRN Campus Caicó, contendo elementos visuais e referências ao curso. O objetivo final é vencer todos os professores para alcançar a formatura.

7. Sistema de Pontuação -
O jogador deve acertar a direção das setas que representam notas musicais. Cada acerto concede 5 pontos, aumentando sua nota (vida).

8. Sistema de Vida -
A vida do jogador é representada por sua nota, iniciando equilibrada com a do professor. Ao errar o ritmo, sua nota diminui enquanto a do professor aumenta, e vice-versa. Se a nota do jogador chegar a zero, ele perde a fase.

9. Controles -
Setas (← ↑ → ↓) → Executar as notas musicais
Enter → Selecionar opções
Esc → Abrir/fechar menu ou sair do jogo

10. Fluxo do Jogo -
O jogo inicia com o jogador enfrentando o professor da primeira fase. Durante a batalha, o jogador deve acertar o maior número possível de movimentos.
A vitória ocorre ao ficar com 60 ou mais na nota final; a derrota acontece quando ficar com menos de 60 na nota final.

11. Regras do Jogo -
O jogador deve atingir a pontuação mínima para vencer cada professor. Caso perca, deverá reiniciar desde a primeira fase, mesmo que já tenha avançado anteriormente.

12. Estrutura do Projeto -
• Organização dos arquivos do jogo:
/assets → Sprites dos personagens, cenários e efeitos visuais
/audio → Trilhas sonoras e efeitos sonoros
/scripts → Lógica do jogo (ritmo, pontuação, mecânicas)
/scenes → Telas (menu, fases, vitória/derrota)
/ui → Interface do usuário
• Separação por responsabilidades:
Player (Aluno) → Entrada do jogador e execução das notas
Professores (Inimigos) → Sequências rítmicas adversárias
Sistema de Ritmo → Sincronização música + inputs
Mapa/Cenário → Ambientação visual
Sistema Geral (Game Manager) → Controle de fases, progresso e vitória
Interface (UI) → Exibição de pontuação, combo e feedback
Sistema de Áudio → Reprodução e sincronização sonora

13. Funcionalidades Mínimas -
O jogo deve conter:
Músicas sincronizadas com as setas
Sistema de nota (vida) funcional
Controles responsivos
Pelo menos um professor, um personagem jogável e um cenário representando o IFRN

14. Melhorias Futuras -
Adição de novas fases e professores
Exploração livre do campus
Seleção de dificuldade
Modo livre (escolha de músicas e fases)

