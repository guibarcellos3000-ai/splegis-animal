/* =========================================================
   SPLegis Animal — página "Leis": busca, filtros e exportação
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const busca = document.getElementById("busca");
  const filtroEsfera = document.getElementById("filtro-esfera");
  const filtroTema = document.getElementById("filtro-tema");
  const ordem = document.getElementById("ordem");
  const lista = document.getElementById("lista-leis");
  const contador = document.getElementById("contador-resultados");
  const btnLimpar = document.getElementById("btn-limpar");
  const btnCSV = document.getElementById("btn-csv");

  // Preenche o filtro de temas com todos os temas existentes
  const temas = [...new Set(LEIS.flatMap((l) => l.temas))].sort((a, b) => a.localeCompare(b, "pt-BR"));
  temas.forEach((tema) => {
    const opt = document.createElement("option");
    opt.value = tema;
    opt.textContent = tema;
    filtroTema.appendChild(opt);
  });

  // Remove acentos e coloca em minúsculas, para a busca encontrar "caca" = "caça"
  const normalizar = (t) => String(t).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  function filtrar() {
    const termo = normalizar(busca.value.trim());
    const esfera = filtroEsfera.value;
    const tema = filtroTema.value;

    const resultado = LEIS.filter((l) => {
      if (esfera && l.esfera !== esfera) return false;
      if (tema && !l.temas.includes(tema)) return false;
      if (!termo) return true;
      const texto = normalizar(
        [l.tipo, l.numero, l.numero.replace(/\./g, ""), l.ano, l.titulo, l.ementa, l.temas.join(" "), l.pontos.join(" ")].join(" ")
      );
      return texto.includes(termo);
    });

    const [campo, direcao] = ordem.value.split("-");
    resultado.sort((a, b) => {
      const cmp = campo === "ano" ? a.ano - b.ano : a.titulo.localeCompare(b.titulo, "pt-BR");
      return direcao === "desc" ? -cmp : cmp;
    });

    return resultado;
  }

  function renderizar() {
    const leis = filtrar();
    contador.textContent =
      leis.length === 1 ? "1 norma encontrada" : `${leis.length} normas encontradas`;

    if (leis.length === 0) {
      lista.innerHTML = `<div class="vazio">Nenhuma norma encontrada com esses filtros.<br>Tente outro termo ou clique em “Limpar filtros”.</div>`;
      return;
    }

    lista.innerHTML = leis
      .map(
        (l) => `
      <article class="lei" id="${escaparHTML(l.id)}">
        <div class="lei-topo">
          <span class="tag tag-${normalizar(l.esfera)}">${escaparHTML(l.esfera)}</span>
          ${l.temas.map((t) => `<span class="tag tag-tema">${escaparHTML(t)}</span>`).join("")}
        </div>
        <h3>${l.tipo === "Constituição"
          ? escaparHTML(l.titulo) + ` (${escaparHTML(l.numero)})`
          : `${escaparHTML(l.tipo)} nº ${escaparHTML(l.numero)}/${l.ano} — ${escaparHTML(l.titulo)}`}</h3>
        <p>${escaparHTML(l.ementa)}</p>
        <details class="detalhes">
          <summary>Principais pontos</summary>
          <ul>${l.pontos.map((p) => `<li>${escaparHTML(p)}</li>`).join("")}</ul>
        </details>
        <p class="meta">
          Data: ${escaparHTML(l.data)} ·
          <a href="${escaparHTML(l.fonte)}" target="_blank" rel="noopener noreferrer">Consultar fonte oficial ↗</a>
        </p>
      </article>`
      )
      .join("");
  }

  /** Gera um arquivo CSV (abre no Excel) com as normas atualmente filtradas. */
  function exportarCSV() {
    const leis = filtrar();
    const cabecalho = ["Esfera", "Tipo", "Número", "Ano", "Data", "Título", "Ementa", "Temas", "Fonte"];
    const celula = (v) => `"${String(v).replace(/"/g, '""')}"`;
    const linhas = leis.map((l) =>
      [l.esfera, l.tipo, l.numero, l.ano, l.data, l.titulo, l.ementa, l.temas.join(", "), l.fonte].map(celula).join(";")
    );
    // ";" como separador e BOM UTF-8 para o Excel em português abrir com acentos corretos
    const csv = "﻿" + [cabecalho.map(celula).join(";"), ...linhas].join("\r\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "splegis-animal-leis.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  [busca, filtroEsfera, filtroTema, ordem].forEach((el) => {
    el.addEventListener("input", renderizar);
    el.addEventListener("change", renderizar);
  });

  btnLimpar.addEventListener("click", () => {
    busca.value = "";
    filtroEsfera.value = "";
    filtroTema.value = "";
    ordem.value = "ano-desc";
    renderizar();
    busca.focus();
  });

  btnCSV.addEventListener("click", exportarCSV);

  // Permite links do tipo leis.html?esfera=Municipal
  const params = new URLSearchParams(location.search);
  if (params.get("esfera")) filtroEsfera.value = params.get("esfera");
  if (params.get("q")) busca.value = params.get("q");

  renderizar();

  // Destaca a lei se vier de um link com #id (ex.: da página inicial)
  if (location.hash) {
    const alvo = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (alvo) {
      alvo.scrollIntoView({ block: "center" });
      alvo.style.outline = "3px solid var(--laranja)";
      const det = alvo.querySelector("details");
      if (det) det.open = true;
    }
  }
});
