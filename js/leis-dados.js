/* =========================================================
   SPLegis Animal — base de dados das leis
   ---------------------------------------------------------
   COMO ADICIONAR UMA NOVA LEI:
   Copie um dos blocos { ... } abaixo, cole no final da lista
   (antes do "];"), separe com vírgula e altere os campos:

     id        -> identificador único, sem espaços
     esfera    -> "Federal", "Estadual" ou "Municipal"
     tipo      -> "Lei", "Lei Complementar", "Decreto", "Constituição"...
     numero    -> número da norma (texto), ex.: "11.977"
     ano       -> ano (número), ex.: 2005
     data      -> data de publicação/assinatura, ex.: "25/08/2005"
     titulo    -> nome curto/popular
     ementa    -> resumo do conteúdo
     temas     -> lista de temas, ex.: ["Maus-tratos", "Cães e gatos"]
     pontos    -> principais dispositivos (lista de frases)
     fonte     -> link para o texto oficial ou portal de consulta

   ATENÇÃO: confira sempre o texto integral e a vigência
   (alterações, revogações, ADIs) no portal oficial antes de
   citar qualquer norma em documento técnico ou parecer.
   ========================================================= */

const FONTE_ALESP = "https://www.al.sp.gov.br/";
const FONTE_PREFEITURA_SP = "https://legislacao.prefeitura.sp.gov.br/";

const LEIS = [
  {
    id: "lei-est-11977-2005",
    esfera: "Estadual",
    tipo: "Lei",
    numero: "11.977",
    ano: 2005,
    data: "25/08/2005",
    titulo: "Código Estadual de Proteção aos Animais",
    ementa:
      "Institui o Código de Proteção aos Animais do Estado de São Paulo, estabelecendo normas para a proteção, defesa e preservação dos animais silvestres, domésticos e domesticados.",
    temas: ["Maus-tratos", "Fauna silvestre", "Animais domésticos"],
    pontos: [
      "Veda práticas que submetam os animais a maus-tratos e crueldade.",
      "Trata da proteção da fauna silvestre, dos animais domésticos e de produção.",
      "Disciplina o transporte, a criação e o uso de animais em diversas atividades."
    ],
    fonte: FONTE_ALESP
  },
  {
    id: "lei-est-12916-2008",
    esfera: "Estadual",
    tipo: "Lei",
    numero: "12.916",
    ano: 2008,
    data: "16/04/2008",
    titulo: "Controle reprodutivo de cães e gatos",
    ementa:
      "Dispõe sobre o controle da reprodução de cães e gatos e dá providências correlatas, vedando a eliminação de animais saudáveis pelos órgãos de controle de zoonoses.",
    temas: ["Cães e gatos", "Saúde pública", "Castração"],
    pontos: [
      "Proíbe a eutanásia de cães e gatos saudáveis por órgãos públicos de controle de zoonoses e congêneres.",
      "Prioriza a esterilização cirúrgica e programas de adoção.",
      "Prevê ações educativas de guarda responsável."
    ],
    fonte: FONTE_ALESP
  },
  {
    id: "lei-est-15316-2014",
    esfera: "Estadual",
    tipo: "Lei",
    numero: "15.316",
    ano: 2014,
    data: "23/01/2014",
    titulo: "Proibição de testes de cosméticos em animais",
    ementa:
      "Proíbe a utilização de animais para desenvolvimento, experimentos e testes de produtos cosméticos, de higiene pessoal, perfumes e seus componentes no Estado de São Paulo.",
    temas: ["Experimentação animal", "Cosméticos"],
    pontos: [
      "Veda o uso de animais em testes de cosméticos, produtos de higiene pessoal e perfumes.",
      "Prevê sanções administrativas a instituições e estabelecimentos infratores."
    ],
    fonte: FONTE_ALESP
  },
  {
    id: "lei-est-16784-2018",
    esfera: "Estadual",
    tipo: "Lei",
    numero: "16.784",
    ano: 2018,
    data: "28/06/2018",
    titulo: "Proibição da caça no Estado de São Paulo",
    ementa:
      "Proíbe a caça, sob qualquer pretexto, forma e para qualquer finalidade, em todo o território do Estado de São Paulo.",
    temas: ["Fauna silvestre", "Caça"],
    pontos: [
      "Proíbe a caça em todas as suas modalidades no território paulista.",
      "Ressalva hipóteses específicas de controle de espécies previstas na legislação."
    ],
    fonte: FONTE_ALESP
  },
  {
    id: "const-est-sp-1989",
    esfera: "Estadual",
    tipo: "Constituição",
    numero: "art. 193",
    ano: 1989,
    data: "05/10/1989",
    titulo: "Constituição do Estado de São Paulo — meio ambiente e fauna",
    ementa:
      "O capítulo do meio ambiente da Constituição Paulista atribui ao Estado o dever de proteger a fauna, vedando práticas que submetam os animais a crueldade.",
    temas: ["Constitucional", "Fauna silvestre", "Maus-tratos"],
    pontos: [
      "Impõe ao Poder Público o dever de proteger a flora e a fauna.",
      "Veda práticas que coloquem em risco a função ecológica, provoquem extinção de espécies ou submetam animais a crueldade."
    ],
    fonte: FONTE_ALESP
  },
  {
    id: "lei-mun-13131-2001",
    esfera: "Municipal",
    tipo: "Lei",
    numero: "13.131",
    ano: 2001,
    data: "18/05/2001",
    titulo: "Criação, guarda e posse de cães e gatos (Município de São Paulo)",
    ementa:
      "Disciplina a criação, propriedade, posse, guarda, uso, transporte e comercialização de cães e gatos no Município de São Paulo.",
    temas: ["Cães e gatos", "Guarda responsável", "Saúde pública"],
    pontos: [
      "Estabelece regras de registro, vacinação e identificação de cães e gatos.",
      "Define responsabilidades do tutor quanto à guarda e ao transporte dos animais.",
      "Regula estabelecimentos que comercializam animais."
    ],
    fonte: FONTE_PREFEITURA_SP
  },
  {
    id: "lei-mun-16897-2018",
    esfera: "Municipal",
    tipo: "Lei",
    numero: "16.897",
    ano: 2018,
    data: "23/05/2018",
    titulo: "Proibição de fogos de artifício com estampido (Município de São Paulo)",
    ementa:
      "Proíbe o manuseio, a utilização, a queima e a soltura de fogos de estampidos e de artifícios, assim como de quaisquer artefatos pirotécnicos de efeito sonoro ruidoso, no Município de São Paulo.",
    temas: ["Fogos de artifício", "Bem-estar animal"],
    pontos: [
      "Proíbe fogos com efeito sonoro ruidoso, permitindo os de efeito apenas visual.",
      "Medida voltada à proteção de animais, pessoas com autismo, idosos e enfermos."
    ],
    fonte: FONTE_PREFEITURA_SP
  },
  {
    id: "cf-1988-art225",
    esfera: "Federal",
    tipo: "Constituição",
    numero: "art. 225, § 1º, VII",
    ano: 1988,
    data: "05/10/1988",
    titulo: "Constituição Federal — vedação à crueldade contra animais",
    ementa:
      "Incumbe ao Poder Público proteger a fauna e a flora, vedadas, na forma da lei, as práticas que submetam os animais a crueldade. Aplica-se a todo o território nacional, inclusive São Paulo.",
    temas: ["Constitucional", "Maus-tratos", "Fauna silvestre"],
    pontos: [
      "Fundamento constitucional da proteção animal no Brasil.",
      "O § 7º (EC 96/2017) trata das práticas desportivas que utilizem animais, desde que manifestações culturais registradas."
    ],
    fonte: "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"
  },
  {
    id: "lei-fed-9605-1998",
    esfera: "Federal",
    tipo: "Lei",
    numero: "9.605",
    ano: 1998,
    data: "12/02/1998",
    titulo: "Lei de Crimes Ambientais",
    ementa:
      "Dispõe sobre as sanções penais e administrativas derivadas de condutas e atividades lesivas ao meio ambiente. O art. 32 tipifica o crime de maus-tratos a animais.",
    temas: ["Maus-tratos", "Crimes ambientais", "Fauna silvestre"],
    pontos: [
      "Art. 29: crimes contra a fauna silvestre (caçar, perseguir, apanhar, comercializar).",
      "Art. 32: praticar ato de abuso, maus-tratos, ferir ou mutilar animais silvestres, domésticos ou domesticados.",
      "Art. 32, § 1º-A (incluído pela Lei 14.064/2020): pena agravada quando se tratar de cão ou gato."
    ],
    fonte: "https://www.planalto.gov.br/ccivil_03/leis/l9605.htm"
  },
  {
    id: "lei-fed-11794-2008",
    esfera: "Federal",
    tipo: "Lei",
    numero: "11.794",
    ano: 2008,
    data: "08/10/2008",
    titulo: "Lei Arouca — uso científico de animais",
    ementa:
      "Regulamenta o inciso VII do § 1º do art. 225 da Constituição Federal, estabelecendo procedimentos para o uso científico de animais e criando o CONCEA.",
    temas: ["Experimentação animal", "Pesquisa científica"],
    pontos: [
      "Cria o Conselho Nacional de Controle de Experimentação Animal (CONCEA).",
      "Exige Comissões de Ética no Uso de Animais (CEUAs) nas instituições."
    ],
    fonte: "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11794.htm"
  },
  {
    id: "lei-fed-14064-2020",
    esfera: "Federal",
    tipo: "Lei",
    numero: "14.064",
    ano: 2020,
    data: "29/09/2020",
    titulo: "Lei Sansão — aumento de pena para maus-tratos a cães e gatos",
    ementa:
      "Altera a Lei nº 9.605/1998 para aumentar as penas cominadas ao crime de maus-tratos aos animais quando se tratar de cão ou gato.",
    temas: ["Maus-tratos", "Cães e gatos", "Crimes ambientais"],
    pontos: [
      "Pena de reclusão de 2 a 5 anos, multa e proibição da guarda para maus-tratos a cães e gatos.",
      "Pena aumentada de 1/6 a 1/3 se ocorrer a morte do animal."
    ],
    fonte: "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14064.htm"
  }
];
