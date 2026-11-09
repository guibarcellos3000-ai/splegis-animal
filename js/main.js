/* =========================================================
   SPLegis Animal — scripts comuns a todas as páginas
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // Menu responsivo (celular)
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector(".nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const aberto = menu.classList.toggle("aberto");
      toggle.setAttribute("aria-expanded", String(aberto));
    });
  }

  // Ano atual no rodapé
  document.querySelectorAll("[data-ano-atual]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Botão "voltar ao topo"
  const topo = document.querySelector(".voltar-topo");
  if (topo) {
    window.addEventListener("scroll", () => {
      topo.classList.toggle("visivel", window.scrollY > 400);
    });
    topo.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  // Estatísticas e destaques da página inicial
  if (typeof LEIS !== "undefined") {
    preencherEstatisticas();
    preencherDestaques();
  }
});

/** Escapa texto para inserção segura em HTML. */
function escaparHTML(texto) {
  return String(texto)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function preencherEstatisticas() {
  const contar = (esfera) => LEIS.filter((l) => !esfera || l.esfera === esfera).length;
  const mapa = {
    total: contar(),
    federal: contar("Federal"),
    estadual: contar("Estadual"),
    municipal: contar("Municipal")
  };
  Object.entries(mapa).forEach(([chave, valor]) => {
    const el = document.querySelector(`[data-stat="${chave}"]`);
    if (el) el.textContent = valor;
  });
}

function preencherDestaques() {
  const alvo = document.getElementById("destaques");
  if (!alvo) return;
  const ids = ["lei-est-11977-2005", "lei-est-12916-2008", "lei-fed-14064-2020"];
  alvo.innerHTML = ids
    .map((id) => LEIS.find((l) => l.id === id))
    .filter(Boolean)
    .map(
      (l) => `
      <article class="card lei-destaque">
        <span class="numero">${escaparHTML(l.tipo)} ${escaparHTML(l.esfera)} nº ${escaparHTML(l.numero)}/${l.ano}</span>
        <h3>${escaparHTML(l.titulo)}</h3>
        <p>${escaparHTML(l.ementa)}</p>
        <a href="leis.html#${encodeURIComponent(l.id)}">Ver detalhes →</a>
      </article>`
    )
    .join("");
}
