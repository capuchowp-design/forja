# FORJA — pronto pra subir no GitHub Pages

## O que tem aqui
```
index.html              ← o app (antigo forja.html, já renomeado)
manifest.json           ← permite instalar como app (tela cheia, sem barra do navegador)
icons/                  ← ícones do app (192, 512, 180 - Apple)
gifs.js                 ← mapa id do exercício → arquivo .webp (25 confirmados)
exercicios/             ← seus 711 arquivos .webp (nomes normalizados)
revisar-manualmente.md  ← 39 exercícios que precisam de conferência manual
nao-casados.txt         ← 669 arquivos que ainda não viraram exercício no app
gerar_manifest.py       ← script que gerou tudo isso (pra rodar de novo se adicionar mais arquivos)
```

## Sobre o tamanho — pode subir tudo tranquilo
- Nenhum arquivo passa de **2,3 MB** (o limite do GitHub é 100 MB por arquivo, e ele já
  avisa a partir de 50 MB). Não precisa de Git LFS.
- O repositório inteiro fica com **~200 MB**, bem abaixo do limite recomendado (1 GB).
- Os 711 arquivos internos foram deixados **soltos** dentro de `exercicios/` (sem
  subpastas), porque era como estavam no seu zip — o app não se importa, ele só
  concatena `exercicios/` + o nome do arquivo do `gifs.js`.

## Passo a passo pra subir

```bash
# 1. crie o repositório no GitHub (pelo site, sem README/gitignore)

# 2. na pasta que você recebeu de mim:
git init
git add -A
git commit -m "FORJA: app + exercícios em webp"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

Se o `git push` travar ou cair no meio (comum em conexões lentas com 711
arquivos), rode `git push` de novo — o Git retoma de onde parou.

## Ativar o GitHub Pages
`Settings → Pages → Source: Deploy from a branch → Branch: main / (root) → Save`

Depois de 1–2 minutos o app estará em:
`https://SEU-USUARIO.github.io/SEU-REPO/`

## Testar a experiência "de app" (imersiva)
1. Abra o link acima no celular.
2. Android (Chrome): menu ⋮ → **Adicionar à tela inicial**.
   iPhone (Safari): botão compartilhar → **Adicionar à Tela de Início**.
3. Abra pelo ícone criado — o app abre em **tela cheia**, sem barra de
   endereço, como um app nativo (isso é o que o `manifest.json` e as meta
   tags que adicionei no `index.html` habilitam).

## O que eu revisei/ajustei no `index.html`
- Adicionei `manifest.json` + ícones + meta tags de PWA (`apple-mobile-web-app-capable`,
  `theme-color`, `mobile-web-app-capable`) — sem isso, "adicionar à tela inicial"
  abre o app dentro do navegador, com a barra de endereço visível.
- `viewport-fit=cover` + `env(safe-area-inset-top/bottom)` no topo e no menu
  inferior — evita que o conteúdo fique atrás do notch/ilha dinâmica ou da
  barra de gestos em iPhones recentes (o rodapé já tratava isso; o topo não).
- O resto do app (modal do exercício, lazy loading das imagens, layout,
  navegação) já estava bem estruturado — não precisei mexer na lógica.
- **Não adicionei service worker** (cache offline): com 200 MB de vídeos,
  cachear tudo localmente é arriscado (esgota o armazenamento do
  navegador em vários celulares). O app já usa `loading="lazy"` +
  cache HTTP normal do navegador, que é a abordagem certa aqui.

## Próximo passo pendente
Veja `revisar-manualmente.md`: 25 exercícios já têm o gif certo linkado,
mas 39 ainda precisam de conferência ou não têm arquivo correspondente
(veja `nao-casados.txt` — 669 arquivos disponíveis). Me manda esse arquivo
de texto que eu expando o banco de exercícios do app pra cobrir os 711.
