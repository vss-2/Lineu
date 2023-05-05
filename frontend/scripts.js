const municipalities = location.href+"/municipalities";
const cidade_class = "cidade";
var cities = {};

let states = {
  BR: "Brasil - Nacional",
  AC: "Acre",
  AL: "Alagoas",
  AM: "Amazonas",
  AP: "Amapá",
  BA: "Bahia",
  CE: "Ceará",
  DF: "Distrito Federal",
  ES: "Espirito Santo",
  GO: "Goiás",
  MA: "Maranhão",
  MG: "Minas Gerais",
  MS: "Mato Grosso Do Sul",
  MT: "Mato Grosso",
  PA: "Pará",
  PB: "Paraíba",
  PE: "Pernambuco",
  PI: "Piauí",
  PR: "Paraná",
  RJ: "Rio De Janeiro",
  RN: "Rio Grande Do Norte",
  RO: "Rondônia",
  RR: "Roraima",
  RS: "Rio Grande Do Sul",
  SC: "Santa Catarina",
  SE: "Sergipe",
  SP: "São Paulo",
  TO: "Tocantins"
}

const raca_cor = {
  1: 'Branca',
  2: 'Preta',
  3: 'Amarela',
  4: 'Parda',
  5: 'Indígena',
  X: 'Cód. Inválido',
  99: 'Sem informação'
};

const comunidade = {
  1: "Povos Quilombolas",
  2: "Agroextrativistas",
  3: "Caatingueiros",
  4: "Caiçaras",
  5: "Comunidades de Fundo e Fecho de Pasto",
  6: "Comunidades do Cerrado",
  7: "Extrativistas",
  8: "Faxinalenses",
  9: "Geraizeiros",
  10: "Marisqueiros",
  11: "Pantaneiros",
  12: "Pescadores Artesanais",
  13: "Pomeranos",
  14: "Povos Ciganos",
  15: "Povos de Terreiro",
  16: "Quebradeiras de Coco-de-Babaçu",
  17: "Retireiros",
  18: "Ribeirinhos",
  19: "Seringueiros",
  20: "Vazanteiros",
  21: "Outros"
};

let escolaridade = {
  1: "Creche",
  2: "Pré-escola (exceto CA)",
  3: "Classe Alfabetizada: CA",
  4: "Ensino Fundamental 1ª a 4ª séries",
  5: "Ensino Fundamental 5ª a 8ª séries",
  6: "Ensino Fundamental Completo",
  7: "Ensino Fundamental Especial",
  8: "Ensino Fundamental, EJA: séries iniciais (Supletivo 1ª a 4ª)",
  9: "Ensino Fundamental, EJA: séries iniciais (Supletivo 5ª a 8ª)",
  10: "Ensino Médio, Médio 2º Ciclo (Científico, Técnico e etc)",
  11: "Ensino Médio Especial",
  12: "Ensino Médio EJA (Supletivo)",
  13: "Superior, Aperfeiçoamento, Especialização, Mestrado, Doutorado",
  14: "Alfabetização para Adultos (Mobral, etc)",
  15: "Nenhum",
  99: "Sem informação"
};

// Adiciona todos os estados ao select
let select_estados = document.getElementById("estados");
for (const key in states) {
  const option = document.createElement("option");
  option.class = "estado";
  option.value = key;
  option.onchange = (e) => fetchCidades(e);
  option.text = states[key];
  select_estados.add(option);
}

let select_raca_cores = document.getElementById("raca-cores");
for (const key in raca_cor) {
  const option = document.createElement("option");
  option.class = "raca-cor";
  option.value = key;
  option.text = raca_cor[key];
  select_raca_cores.add(option);
}

let select_comunidades = document.getElementById("comunidades");
for (const key in comunidade) {
  const option = document.createElement("option");
  option.class = "comunidade";
  option.value = key;
  option.text = comunidade[key];
  select_comunidades.add(option);
}

let select_escolaridades = document.getElementById("escolaridades");
for (const key in escolaridade) {
  const option = document.createElement("option");
  option.class = "escolaridade";
  option.value = key;
  option.text = escolaridade[key];
  select_escolaridades.add(option);
}

function buildJSON() {
  return {
    minAge: document.getElementById('min-age-input').value,
    maxAge: document.getElementById('max-age-input').value,
    exactAge: document.getElementById('exact-age-input').value,
    genre: document.getElementById('generos').value,
    education: document.getElementById('escolaridades').value,
    etnicity: document.getElementById('raca-cores').value,
    community: document.getElementById('comunidades').value,
    minDate: document.getElementById('min-appointment-date').value,
    maxDate: document.getElementById('max-appointment-date').value,
    minWeight: document.getElementById('min-weight-input').value,
    maxWeight: document.getElementById('max-weight-input').value,
    minHeight: document.getElementById('min-height-input').value,
    maxHeight: document.getElementById('max-height-input').value,
    minIMC: document.getElementById('min-imc-input').value,
    maxIMC: document.getElementById('max-imc-input').value,
    state: document.getElementById('estados').value,
    city: document.getElementById('cidades').value,
    CNES: document.getElementById('CNES').value
  }
}

let optionSelected = '';

function citySelected(sel) {
  optionSelected = sel.options[sel.selectedIndex].text;
}

fetch(municipalities, {mode: 'cors', 'Access-Control-Allow-Origin': '*'})
  .then((response) => response.json())
  .then((data) => {
    cities = data;
    // console.log(data);
  })
  .catch((error) => {
    console.error(error);
  });

function fetchCidades(event) {
  // Remove all cities if choose another state (avoid mixing)
  function deleteCidadeOptions() {
    document.getElementById('cidades').innerHTML = "<option value=\"\"></option>";
  }
  deleteCidadeOptions();
  
  let selected_state = document.getElementById("estados");
  selected_state = selected_state.value;
  if (selected_state.length != 2) {
    return;
  }
  const cidades = document.getElementById("cidades");
  let count = 0;
  for (let c in cities[selected_state]) {
    const option = document.createElement("option");
    option.class = cidade_class;
    option.value = Object.values(cities[selected_state][count]);
    option.text = Object.keys(Object.values(cities[selected_state])[count])[0];
    cidades.add(option);
    count += 1;
  }
}

// Keep cities in cache to avoid exhaustive fetching
if ("caches" in window) {
  caches.open("lineu-cache").then(function (cache) {
    cache.add(municipalities).then(function () {
      console.log("Municípios salvos!");
    });
  });
} else {
  alert(
    "Seu navegador não é compatível com Lineu, tente ativar o JavaScript, permitir acesso ao cache ou trocar de navegador!"
  );
}

function hideResults(){
  document.getElementById('card-holder').style.display = 'none';
  document.getElementById('query').style.display = 'block';
}

const navlang = navigator.language;

const form = document.querySelector('#query');
form.addEventListener('submit', (event) => {
  // prevent the form from submitting in the default way
  event.preventDefault();

  let fields = buildJSON();

  if(fields.estado == '' && fields.cidade == ''){
    alert('Selecione um estado ou cidade!');
  }

  fetch('/data', { // make an HTTP request to the server
    method: 'POST',
    body: JSON.stringify(fields),
    headers: {
      "Content-Type": "application/json",
      mode: 'no-cors', 
      'Access-Control-Allow-Origin': '*'
    },
  })
  .then(response => response.json())
  .then(blob => {
    document.getElementById('city-data').innerHTML = "";
    document.getElementById('card-holder').style.display = "block";
    const img = document.getElementById('map-image');
    img.src = "data:image/png;base64,"+blob.image;
    let unordered_list = document.createElement("ul");
    let count = 0;
    let itens = ['Peso', 'Altura', 'Idade', 'IMC'];

    let cityStateTitle = document.createElement('h3');
    cityStateTitle.innerText = optionSelected + '-' + document.getElementById('estados').value;

    try {
      blob.data = JSON.parse(blob.data);
      blob.cnes = JSON.parse(blob.cnes);
      cityStateTitle.innerText += ' (' + blob.data['NU_PESO']['count'] + ' registros)';
      console.log(blob.data);
    } catch (error) { 
      /* TODO: fix error on JSON.parse: 
        SyntaxError: "[object Object]" is not valid JSON
      */
    }

    for (let statistic of ['NU_PESO', 'NU_ALTURA', 'NU_IDADE_ANO', 'DS_IMC']){
        let new_ul_item = document.createElement("li");

        function generateList(new_ul_item){
            new_ul_item.innerText += itens[count] + '\n';
            if(blob.data[statistic]['mean']){
              new_ul_item.innerHTML += itens[count] + ' médio(a): ' + blob.data[statistic]['mean'].toLocaleString(navlang, {maximumFractionDigits: 2, minimumFractionDigits: 2});
              new_ul_item.innerHTML += '<br>';
            }
            if(blob.data[statistic]['std']){
              new_ul_item.innerHTML += 'Desvio padrão: ' + blob.data[statistic]['std'].toLocaleString(navlang, {maximumFractionDigits: 2, minimumFractionDigits: 2});
              new_ul_item.innerHTML += '<br>';
            }
            new_ul_item.innerHTML += 'Quartis (25, 50, 75)%: ' + blob.data[statistic]['25%'].toLocaleString(navlang, {maximumFractionDigits: 2, minimumFractionDigits: 2}) + '; ' + blob.data[statistic]['50%'].toLocaleString(navlang, {maximumFractionDigits: 2, minimumFractionDigits: 2}) + '; ' + blob.data[statistic]['75%'].toLocaleString(navlang, {maximumFractionDigits: 2, minimumFractionDigits: 2});
            new_ul_item.innerHTML += '<br><br>';
        }
        generateList(new_ul_item);
        unordered_list.appendChild(new_ul_item);
        count += 1;
    }
    let cnesDiv = document.createElement('div');
    cnesDiv.className = "cnes-list";
    let cnesList = document.createElement('ol');
    cnesList.className = 'ol-list'
    cnesDiv.appendChild(cnesList);
    
    for(let cnes of Object.keys(blob.cnes)){
      if(cnes.length > 8){
        let itemCnes = document.createElement('li');
        itemCnes.innerHTML = `<a href="https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=${cnes.slice(0, -2)}">${cnes.slice(0,-2)}</a>: ${blob.cnes[cnes]} exames`
        cnesList.appendChild(itemCnes);
      }
    }
    
    let returnButton = document.createElement('button');
    returnButton.innerText = 'Voltar';
    returnButton.onclick = () => hideResults();
    returnButton.id = 'search-button';
    document.getElementById('query').style.display = 'none';
    document.getElementById('city-data').appendChild(cityStateTitle);
    document.getElementById('city-data').appendChild(unordered_list);
    document.getElementById('city-data').appendChild(cnesDiv);
    document.getElementById('city-data').appendChild(returnButton);
  })
  .catch(error => {
    console.error(error); 
    // TODO: handle errors
  });
});

function toggleAgeFields() {
  var selectedAgeValue = document.getElementById("age-select").value;
  var minAgeField = document.getElementById("min-age");
  var maxAgeField = document.getElementById("max-age");
  var exactAgeField = document.getElementById("exact-age");

  if (selectedAgeValue === "age range") {
    minAgeField.style.display = "inline-block";
    maxAgeField.style.display = "inline-block";
    exactAgeField.style.display = "none";
    exactAgeField.value = "";
  } else if (selectedAgeValue === "age equal") {
    minAgeField.style.display = "none";
    maxAgeField.style.display = "none";
    exactAgeField.style.display = "inline-block";
    minAgeField.value = "";
    maxAgeField.value = "";
  } else {
    minAgeField.style.display = "none";
    maxAgeField.style.display = "none";
    exactAgeField.style.display = "none";
  }
}
