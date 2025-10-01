// Use the same origin as the page to avoid CORS/host mismatch (localhost vs 127.0.0.1)
const apiBase = window.location.origin;

const categoryEl = document.getElementById("category");
const fromEl = document.getElementById("fromUnit");
const toEl = document.getElementById("toUnit");
const valueEl = document.getElementById("value");
const formEl = document.getElementById("convertForm");
const resultEl = document.getElementById("resultText");
const toastEl = document.getElementById("toast");

const UNIT_OPTIONS = {
  temperature: [
    { v: "c", l: "Celsius (C)" },
    { v: "f", l: "Fahrenheit (F)" },
    { v: "k", l: "Kelvin (K)" },
  ],
  distance: [
    { v: "m", l: "Metro (m)" },
    { v: "km", l: "Quilômetro (km)" },
    { v: "mi", l: "Milha (mi)" },
  ],
  weight: [
    { v: "kg", l: "Quilograma (kg)" },
    { v: "lb", l: "Libra (lb)" },
  ],
};

function showToast(message, type = "error") {
  toastEl.textContent = message;
  toastEl.className = `toast ${type}`;
  toastEl.classList.add("show");
  setTimeout(() => toastEl.classList.remove("show"), 2800);
}

function populateUnits(category) {
  fromEl.innerHTML = "";
  toEl.innerHTML = "";
  UNIT_OPTIONS[category].forEach((opt) => {
    const o1 = document.createElement("option");
    o1.value = opt.v;
    o1.textContent = opt.l;
    const o2 = o1.cloneNode(true);
    fromEl.appendChild(o1);
    toEl.appendChild(o2);
  });
  // Evita from == to por padrão
  if (toEl.options.length > 1) toEl.selectedIndex = 1;
}

categoryEl.addEventListener("change", (e) => {
  populateUnits(e.target.value);
  resultEl.textContent = "—";
});

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const category = categoryEl.value;
  const fromUnit = fromEl.value;
  const toUnit = toEl.value;
  const rawValue = valueEl.value.trim();

  if (!rawValue) {
    showToast("Informe um valor para converter.");
    return;
  }

  const value = Number(rawValue.replace(",", "."));
  if (Number.isNaN(value)) {
    showToast("Valor inválido. Use números (ex: 12.34).");
    return;
  }

  try {
    const url = new URL(`${apiBase}/convert`);
    url.searchParams.set("category", category);
    url.searchParams.set("from_unit", fromUnit);
    url.searchParams.set("to_unit", toUnit);
    url.searchParams.set("value", String(value));

    const res = await fetch(url.toString());
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || "Erro na requisição.");
    }
  const data = await res.json();
  resultEl.textContent = `${value} ${fromUnit} = ${Number(data.result.toFixed(6))} ${toUnit}`;
    // animação
    resultEl.classList.remove("pop");
    // forçar reflow
    void resultEl.offsetWidth;
    resultEl.classList.add("pop");
  } catch (err) {
    console.error(err);
    showToast("Não foi possível converter. Verifique os dados e a API.");
  }
});

// Inicializa
populateUnits(categoryEl.value);