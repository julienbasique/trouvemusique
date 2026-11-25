const $ = (id) => document.getElementById(id);
let questions = [];
let reponses = {};
let index = 0;
let session_id = null;
let lecteur = null;

async function commencer() {
  const r = await fetch("/api/questions");
  const d = await r.json();
  questions = d.questions;
  index = 0;
  reponses = {};
  $("quiz").classList.remove("hidden");
  $("resultats").classList.add("hidden");
  montrerQuestion();
}

function montrerQuestion() {
  const q = questions[index];
  $("progress-barre").style.width = (index / questions.length * 100) + "%";
  $("compteur").textContent = `Question ${index + 1} / ${questions.length}`;
  $("question-libelle").textContent = q.question;
  const opts = $("options");
  opts.innerHTML = "";
  if (q.type === "texte") {
    opts.classList.add("hidden");
    $("artiste-bloc").classList.remove("hidden");
    $("artiste-input").value = "";
    $("artiste-input").focus();
    return;
  }
  opts.classList.remove("hidden");
  $("artiste-bloc").classList.add("hidden");
  for (const o of q.options) {
    const b = document.createElement("button");
    b.className = "option";
    b.textContent = o.libelle;
    b.onclick = () => choisir(o.id);
    opts.appendChild(b);
  }
}

function choisir(id) {
  reponses[questions[index].id] = id;
  index++;
  if (index < questions.length) montrerQuestion();
  else {
    // dernière question = texte : le bouton "Voilà" déclenche la fin
    montrerQuestion();
  }
}

async function terminer() {
  const artiste = ($("artiste-input").value || "").trim();
  $("quiz").classList.add("hidden");
  $("tag-etape").textContent = "on cherche…";
  const r = await fetch("/api/resultat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...reponses, artiste }),
  });
  const d = await r.json();
  session_id = d.session_id;
  afficherResultats(d);
}

function afficherResultats(d) {
  $("resultats").classList.remove("hidden");
  $("tag-etape").textContent = "voilà ta musique";
  $("styles-grille").innerHTML = (d.styles || []).map((s, i) =>
    `<div class="style${i === 0 ? " top" : ""}">${s.nom}${i === 0 ? " · le plus proche" : ""}</div>`).join("");
  $("raisons").innerHTML = (d.raisons || []).map((r) =>
    `<li>${r}</li>`).join("");
  $("raisons").classList.toggle("hidden", !(d.raisons || []).length);
  renderPistes(d.pistes || []);
  $("note-raffinage").textContent = "";
  $("tag-etape").textContent = "écoutem, dis ce qui te parle";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderPistes(pistes) {
  $("pistes").innerHTML = pistes.map((p, i) => `
    <div class="piste" data-i="${i}">
      <button class="play" data-preview="${p.preview}" aria-label="écouter 30 s">▶</button>
      <img class="pochette" src="${p.image}" loading="lazy" alt="">
      <div class="piste-info">
        <div class="piste-titre">${p.titre}</div>
        <div class="piste-artiste">${p.artiste} — ${p.album}</div>
      </div>
      <span class="piste-style">${p.style_nom || ""}</span>
      <a class="piste-lien" href="${p.lien}" target="_blank" rel="noopener">entier ↗</a>
      <button class="retour aime" data-artiste="${p.artiste}" data-titre="${p.titre}" data-style="${p.style_cle}">👍</button>
      <button class="retour pas" data-artiste="${p.artiste}" data-titre="${p.titre}" data-style="${p.style_cle}">👎</button>
    </div>`).join("");
}

// lecture : un seul lecteur, bouton ▶/■
$("lecteur") ? null : null;
document.addEventListener("click", async (e) => {
  const play = e.target.closest(".play");
  if (play) {
    const audio = $("lecteur");
    if (audio.src === play.dataset.preview && !audio.paused) {
      audio.pause();
      play.textContent = "▶";
      return;
    }
    audio.src = play.dataset.preview;
    audio.play();
    document.querySelectorAll(".play").forEach((b) => b.textContent = "▶");
    play.textContent = "■";
    audio.onended = () => play.textContent = "▶";
    return;
  }
  const retour = e.target.closest(".retour");
  if (retour && session_id) {
    retour.disabled = true;
    const r = await fetch("/api/retour", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id,
        artiste: retour.dataset.artiste,
        titre: retour.dataset.titre,
        style_cle: retour.dataset.style,
        action: retour.classList.contains("aime") ? "aime" : "pas",
      }),
    });
    const d = await r.json();
    renderPistes(d.pistes || []);
    $("note-raffinage").textContent = d.note || "";
  }
});

$("btn-fini").onclick = terminer;
$("artiste-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") terminer();
});
$("btn-recommencer").onclick = commencer;

commencer();
