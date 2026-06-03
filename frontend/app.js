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

function print(text, highlight = false) {
  const line = document.createElement("div");

  if (highlight) {
    if (currentRisk === "warning") {
      line.classList.add("bold-warning");
    } else if (currentRisk === "danger") {
      line.classList.add("bold-danger");
    } else {
      line.classList.add("bold-safe");
    }
  }

  line.innerHTML = text;

  output.appendChild(line);

  // espaçamento visual
  line.style.marginBottom = "6px";

  output.scrollTop = output.scrollHeight;
}

async function renderResult(data) {
  clearOutput();

  const prediction = (data.prediction || "").toLowerCase();
  const riskLevel = (data.risk_level || "").toLowerCase();

  if (prediction.includes("suspeita")) {
    setRiskTheme("suspeita");
  } else if (
    prediction.includes("phishing") ||
    riskLevel.includes("risco")
  ) {
    setRiskTheme("phishing");
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

  // 🔥 agora sim: destaques separados (CORRETO)
  print(`LEGITIMATE PROB: ${data.legitimate_probability}`, true);
  print(`PHISHING PROB: ${data.phishing_probability}`, true);

  await delay(300);

  if (prediction.includes("suspeita")) {
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