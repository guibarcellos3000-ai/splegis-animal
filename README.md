# SPLegis Animal

Site estático (HTML, CSS e JavaScript puros) do projeto **SPLegis Animal**, que reúne a legislação de proteção animal aplicável ao Estado e ao Município de São Paulo.

## Páginas

| Arquivo        | Conteúdo |
|----------------|----------|
| `index.html`   | Página inicial: apresentação, números do acervo, normas em destaque e canais de denúncia |
| `leis.html`    | Lista de leis com busca, filtros (esfera, tema), ordenação e botão para baixar planilha (CSV, abre no Excel) |
| `contato.html` | Formulário de contato com validação |

## Estrutura

```
css/style.css      -> visual do site (cores no início do arquivo, em :root)
js/leis-dados.js   -> BASE DE DADOS DAS LEIS (edite aqui para incluir/alterar normas)
js/main.js         -> menu, rodapé e destaques da página inicial
js/leis.js         -> busca, filtros e exportação CSV
js/contato.js      -> validação e envio do formulário
```

## Como ver o site

Basta abrir o arquivo `index.html` no navegador (duplo clique). Não precisa instalar nada.

## Como adicionar uma lei

Abra `js/leis-dados.js`, copie um bloco `{ ... }` existente, cole no final da lista e altere os campos. As instruções estão no topo do arquivo.

## Configurar o e-mail de contato

Em `js/contato.js`, troque `EMAIL_DESTINO` pelo e-mail oficial do projeto. Opcionalmente, preencha `ENDPOINT_FORMULARIO` com o endereço de um serviço como Formspree para receber as mensagens sem abrir o programa de e-mail do visitante.

## Publicação

Por ser um site estático, pode ser publicado gratuitamente no GitHub Pages (Settings → Pages → branch principal, pasta raiz).

> Aviso: os resumos são informativos. Confira sempre o texto integral e a vigência das normas nos portais oficiais (ALESP, Legislação Municipal de SP, Planalto).
