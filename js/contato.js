/* =========================================================
   SPLegis Animal — formulário de contato
   ---------------------------------------------------------
   O site é estático (sem servidor). Ao enviar, o formulário
   abre o programa de e-mail do visitante com a mensagem pronta.
   Para receber as mensagens direto, sem abrir o e-mail, você
   pode usar um serviço gratuito como Formspree ou Netlify Forms
   e colocar o endereço dele em ENDPOINT_FORMULARIO.
   ========================================================= */

const EMAIL_DESTINO = "contato@splegisanimal.org.br"; // TROQUE pelo e-mail oficial do projeto
const ENDPOINT_FORMULARIO = ""; // ex.: "https://formspree.io/f/xxxxxxx" (opcional)

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-contato");
  if (!form) return;

  const sucesso = document.getElementById("msg-sucesso");
  const mensagem = form.elements.mensagem;
  const contadorChars = document.getElementById("contador-chars");
  const LIMITE = Number(mensagem.getAttribute("maxlength")) || 2000;

  document.querySelectorAll("[data-email-destino]").forEach((el) => {
    el.textContent = EMAIL_DESTINO;
    if (el.tagName === "A") el.href = `mailto:${EMAIL_DESTINO}`;
  });

  mensagem.addEventListener("input", () => {
    contadorChars.textContent = `${mensagem.value.length}/${LIMITE}`;
  });

  const regras = {
    nome: (v) => (v.trim().length >= 3 ? "" : "Informe seu nome (mínimo de 3 letras)."),
    email: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Informe um e-mail válido."),
    assunto: (v) => (v ? "" : "Escolha um assunto."),
    mensagem: (v) => (v.trim().length >= 10 ? "" : "Escreva uma mensagem com pelo menos 10 caracteres."),
    consentimento: (_, el) => (el.checked ? "" : "É preciso concordar com o uso dos dados para responder.")
  };

  function validarCampo(nome) {
    const el = form.elements[nome];
    const erro = regras[nome](el.value, el);
    const caixa = el.closest(".campo");
    caixa.classList.toggle("invalido", Boolean(erro));
    caixa.querySelector(".msg-erro").textContent = erro;
    el.setAttribute("aria-invalid", String(Boolean(erro)));
    return !erro;
  }

  Object.keys(regras).forEach((nome) => {
    form.elements[nome].addEventListener("blur", () => validarCampo(nome));
    form.elements[nome].addEventListener("change", () => validarCampo(nome));
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    sucesso.hidden = true;

    const validos = Object.keys(regras).map(validarCampo);
    if (validos.includes(false)) {
      form.querySelector(".invalido input, .invalido select, .invalido textarea")?.focus();
      return;
    }

    const dados = {
      nome: form.elements.nome.value.trim(),
      email: form.elements.email.value.trim(),
      instituicao: form.elements.instituicao.value.trim(),
      assunto: form.elements.assunto.value,
      mensagem: mensagem.value.trim()
    };

    if (ENDPOINT_FORMULARIO) {
      try {
        const resp = await fetch(ENDPOINT_FORMULARIO, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(dados)
        });
        if (!resp.ok) throw new Error(resp.statusText);
        sucesso.textContent = "Mensagem enviada com sucesso! Responderemos em breve.";
      } catch {
        alert("Não foi possível enviar agora. Tente novamente ou escreva para " + EMAIL_DESTINO);
        return;
      }
    } else {
      const corpo =
        `Nome: ${dados.nome}\nE-mail: ${dados.email}\n` +
        (dados.instituicao ? `Instituição: ${dados.instituicao}\n` : "") +
        `\n${dados.mensagem}`;
      window.location.href =
        `mailto:${EMAIL_DESTINO}?subject=${encodeURIComponent("[SPLegis Animal] " + dados.assunto)}` +
        `&body=${encodeURIComponent(corpo)}`;
      sucesso.textContent =
        "Pronto! Abrimos seu programa de e-mail com a mensagem preenchida — é só clicar em Enviar.";
    }

    sucesso.hidden = false;
    form.reset();
    contadorChars.textContent = `0/${LIMITE}`;
    sucesso.scrollIntoView({ block: "center", behavior: "smooth" });
  });
});
