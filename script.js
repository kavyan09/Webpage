const data = {
  us: {
    "Alabama":"Montgomery","Alaska":"Juneau","Arizona":"Phoenix","Arkansas":"Little Rock","California":"Sacramento",
    "Colorado":"Denver","Connecticut":"Hartford","Delaware":"Dover","Florida":"Tallahassee","Georgia":"Atlanta",
    "Hawaii":"Honolulu","Idaho":"Boise","Illinois":"Springfield","Indiana":"Indianapolis","Iowa":"Des Moines",
    "Kansas":"Topeka","Kentucky":"Frankfort","Louisiana":"Baton Rouge","Maine":"Augusta","Maryland":"Annapolis",
    "Massachusetts":"Boston","Michigan":"Lansing","Minnesota":"St. Paul","Mississippi":"Jackson","Missouri":"Jefferson City",
    "Montana":"Helena","Nebraska":"Lincoln","Nevada":"Carson City","New Hampshire":"Concord","New Jersey":"Trenton",
    "New Mexico":"Santa Fe","New York":"Albany","North Carolina":"Raleigh","North Dakota":"Bismarck","Ohio":"Columbus",
    "Oklahoma":"Oklahoma City","Oregon":"Salem","Pennsylvania":"Harrisburg","Rhode Island":"Providence","South Carolina":"Columbia",
    "South Dakota":"Pierre","Tennessee":"Nashville","Texas":"Austin","Utah":"Salt Lake City","Vermont":"Montpelier",
    "Virginia":"Richmond","Washington":"Olympia","West Virginia":"Charleston","Wisconsin":"Madison","Wyoming":"Cheyenne",
    "District of Columbia":"Washington, D.C."},
  india: {
    "Andhra Pradesh":"Amaravati","Arunachal Pradesh":"Itanagar","Assam":"Dispur","Bihar":"Patna","Chhattisgarh":"Raipur",
    "Goa":"Panaji","Gujarat":"Gandhinagar","Haryana":"Chandigarh","Himachal Pradesh":"Shimla","Jharkhand":"Ranchi",
    "Karnataka":"Bengaluru","Kerala":"Thiruvananthapuram","Madhya Pradesh":"Bhopal","Maharashtra":"Mumbai","Manipur":"Imphal",
    "Meghalaya":"Shillong","Mizoram":"Aizawl","Nagaland":"Kohima","Odisha":"Bhubaneswar","Punjab":"Chandigarh",
    "Rajasthan":"Jaipur","Sikkim":"Gangtok","Tamil Nadu":"Chennai","Telangana":"Hyderabad","Tripura":"Agartala",
    "Uttar Pradesh":"Lucknow","Uttarakhand":"Dehradun","West Bengal":"Kolkata",
    "Andaman and Nicobar Islands":"Port Blair","Chandigarh (UT)":"Chandigarh","Dadra and Nagar Haveli and Daman and Diu":"Daman",
    "Delhi":"New Delhi","Jammu and Kashmir":"Srinagar","Ladakh":"Leh","Puducherry":"Puducherry","Lakshadweep":"Kavaratti"},
  uk: {
    "England":"London","Scotland":"Edinburgh","Wales":"Cardiff","Northern Ireland":"Belfast"}
}

const funFacts = {
  "Sacramento":"Sacramento started as a Gold Rush town and has a historic riverfront.",
  "New Delhi":"New Delhi is home to India Gate and the grand Rashtrapati Bhavan.",
  "London":"London has the famous River Thames and a long history back to Roman times.",
  "Bengaluru":"Bengaluru is known as India’s tech hub — " + "" + "Silicon Valley of India.",
  "Albany":"Albany is one of the oldest surviving settlements of the original British thirteen colonies.",
  "Edinburgh":"Edinburgh has a castle on a volcanic rock — great for imagining knights!",
  "Austin":"Austin is famous for music and live concerts — 'Keep Austin Weird' is its motto.",
  "Chennai":"Chennai has beautiful temples and a long coastline on the Bay of Bengal.",
  "Mumbai":"Mumbai is India's largest city and home to Bollywood films.",
}

// UI elements
const countrySelect = document.getElementById('country');
const stateInput = document.getElementById('stateInput');
const suggestions = document.getElementById('suggestions');
const findBtn = document.getElementById('findBtn');
const randomBtn = document.getElementById('randomBtn');
const flagEl = document.getElementById('flag');
const stateNameEl = document.getElementById('stateName');
const capitalNameEl = document.getElementById('capitalName');
const funFactEl = document.getElementById('funFact');
const speakBtn = document.getElementById('speakBtn');
const againBtn = document.getElementById('againBtn');
const card = document.querySelector('.card');

function normalize(s){return s.trim().toLowerCase();}

function countryToEmoji(c){
  if(c==='us') return '🇺🇸';
  if(c==='india') return '🇮🇳';
  if(c==='uk') return '🇬🇧';
  return '🌍';
}

function populateSuggestions(){
  const c = countrySelect.value;
  suggestions.innerHTML = '';
  Object.keys(data[c]).forEach(k=>{
    const opt = document.createElement('option');
    opt.value = k;
    suggestions.appendChild(opt);
  });
}

function findCapital(query, countryKey){
  if(!query) return null;
  const map = data[countryKey];
  const q = normalize(query);
  // exact match
  for(const k of Object.keys(map)){
    if(normalize(k) === q) return {state:k,capital:map[k]};
  }
  // startswith
  for(const k of Object.keys(map)){
    if(normalize(k).startsWith(q)) return {state:k,capital:map[k]};
  }
  // includes
  for(const k of Object.keys(map)){
    if(normalize(k).includes(q)) return {state:k,capital:map[k]};
  }
  return null;
}

function showResult(item, countryKey){
  if(!item){
    stateNameEl.textContent = 'Not found';
    capitalNameEl.textContent = 'Try another name or pick from suggestions.';
    funFactEl.textContent = 'Tip: try a full state name like "California" or "Karnataka".';
    flagEl.textContent = countryToEmoji(countryKey);
    card.classList.remove('hidden');
    return;
  }
  stateNameEl.textContent = item.state;
  capitalNameEl.textContent = item.capital;
  funFactEl.textContent = funFacts[item.capital] || `Fun fact: ${item.state} is interesting — explore more!`;
  flagEl.textContent = countryToEmoji(countryKey);
  card.classList.remove('hidden');
}

findBtn.addEventListener('click',()=>{
  const countryKey = countrySelect.value;
  const q = stateInput.value;
  const item = findCapital(q,countryKey);
  showResult(item,countryKey);
});

randomBtn.addEventListener('click',()=>{
  const c = countrySelect.value;
  const keys = Object.keys(data[c]);
  const state = keys[Math.floor(Math.random()*keys.length)];
  const capital = data[c][state];
  stateInput.value = state;
  showResult({state,capital}, c);
});

speakBtn.addEventListener('click',()=>{
  const text = `${stateNameEl.textContent}. Capital is ${capitalNameEl.textContent}.`;
  if('speechSynthesis' in window){
    const ut = new SpeechSynthesisUtterance(text);
    ut.rate = 0.95;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(ut);
  } else {
    alert('Speech not available on this device.');
  }
});

againBtn.addEventListener('click',()=>{
  card.classList.add('hidden');
  stateInput.value = '';
  stateInput.focus();
});

countrySelect.addEventListener('change',()=>{
  populateSuggestions();
  card.classList.add('hidden');
  stateInput.value = '';
});

stateInput.addEventListener('input',()=>{
  // live attempt suggestion: show if a good match
  const cur = stateInput.value;
  const res = findCapital(cur, countrySelect.value);
  if(res) showResult(res, countrySelect.value);
});

// initialize
populateSuggestions();

// make Enter press behave like Find
stateInput.addEventListener('keydown', e=>{
  if(e.key==='Enter'){
    findBtn.click();
    e.preventDefault();
  }
});
