const output = document.getElementById("output");
const cmd = document.getElementById("cmd");
const terminal = document.querySelector(".terminal");
let currentRisk = "safe";

function clearOutput() {
  output.innerHTML = "";
}

function print(text) {
  output.innerHTML += text + "\n";
  output.scrollTop = output.scrollHeight;
}

function typeText(text, speed = 20) {
  let i = 0;

  const line = document.createElement("div");
  output.appendChild(line);

  function tick() {
    if (i < text.length) {
      line.innerHTML += text[i++];
      setTimeout(tick, speed);
    }
  }

  tick();
}

function createBar(value, max = 100, size = 20) {
  const percent = Math.round((value / max) * 100);
  const filled = Math.round((percent / 100) * size);
  const empty = size - filled;

  const bar =
    "█".repeat(filled) +
    "░".repeat(empty);

  return `${bar} ${percent.toFixed(2)}%`;
}

function setRiskTheme(level) {
  terminal.classList.remove("warning", "danger");

  currentRisk = "safe";

  if (level === "suspeita") {
    terminal.classList.add("warning");
    currentRisk = "warning";
  }

  if (level === "phishing") {
    terminal.classList.add("danger");
    currentRisk = "danger";
  }
}

async function analyzeURL(url) {
  const res = await fetch("http://localhost:8000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  });

  return await res.json();
}

// regra simples e compatível com teu ML
function isURL(text) {
  return text.includes(".");
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function print(text, type = "normal") {
  const line = document.createElement("div");

  line.innerHTML = text;

  if (type === "safe") {
    line.classList.add("bold-safe");
  } else if (type === "warning") {
    line.classList.add("bold-warning");
  } else if (type === "danger") {
    line.classList.add("bold-danger");
  }

  line.style.marginBottom = "6px";

  output.appendChild(line);
  output.scrollTop = output.scrollHeight;
}

async function animateBar(label, value, type = "safe") {
  const steps = 20;
  const target = parseFloat(value);

  for (let i = 0; i <= steps; i++) {
    const current = (target / steps) * i;
    const bar = createBar(current);

    print(`${label}: ${bar}`, type);

    await delay(40);
    output.removeChild(output.lastChild);
  }

  print(`${label}: ${createBar(target)}`, type);
}

async function renderResult(data) {
  terminal.classList.remove("warning", "danger");
  clearOutput();

  const prediction = (data.prediction || "").toLowerCase();

  const isLegit =
    prediction.includes("legítima") ||
    prediction.includes("legitima") ||
    prediction.includes("safe");

  const isPhishing =
    prediction.includes("phishing");

  const isSuspicious =
    prediction.includes("suspeita");

  if (isPhishing) {
    setRiskTheme("phishing");
  } else if (isSuspicious) {
    setRiskTheme("suspeita");
  } else if (isLegit) {
    setRiskTheme("baixo");
  } else {
    setRiskTheme("baixo");
  }
  const lines = [
    "[ANALYZING TARGET...]",
    "",
    `PREDICTION: ${data.prediction}`,
    `RISK LEVEL: ${data.risk_level}`,
    "",
  ];

  for (let line of lines) {
    print(line);
    await delay(400);
  }

  await animateBar("LEGITIMATE PROB", data.legitimate_probability, "safe");
  await animateBar("PHISHING PROB", data.phishing_probability, "safe");

  await delay(300);

  if (isPhishing || isSuspicious) {
    typeText("⚠ THREAT DETECTED: PHISHING NODE");
    await delay(300);
    typeText("INITIATING COUNTER-TRACE...");
    await delay(300);
    typeText("TARGET FLAGGED AS MALICIOUS");
  } else {
    typeText("SAFE NODE CONFIRMED");
    typeText("NO THREATS DETECTED");
  }
}

cmd.addEventListener("keydown", async (e) => {
  if (e.key === "Enter") {
    const value = cmd.value.trim();

    print("> " + value);

    if (isURL(value)) {
      try {
        const result = await analyzeURL(value);
        renderResult(result);
      } catch (err) {
        print("ERROR: API UNREACHABLE");
      }
    } else {
      print("unknown command");
    }

    cmd.value = "";
  }
});

// boot sequence
print("SYSTEM READY...");
print("AWAITING TARGET INPUT...");