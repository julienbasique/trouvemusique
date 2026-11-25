const $ = (id) => document.getElementById(id);
let questions = [];
let reponses = {};
let index = 0;
let session_id = null;
let en_avance = false;          // garde anti double-clic entre questions

async function commencer() {
  const lecteur = $("lecteur");
  if (lecteur.src) { lecteur.pause(); lecteur.src = ""; }
  const r = await fetch("/api/questions");
  const d = await r.json();
  questions = d.questions;
  index = 0;
  reponses = {};
  $("resultats").classList.add("hidden");
  $("chargement").classList.add("hidden");
  $("quiz").classList.remove("hidden");
  $("tag-etape").textContent = "14 réponses clic + 1 artiste si tu veux";
  montrerQuestion();
}

function montrerQuestion() {
  const q = questions[index];
  $("progress-barre").style.width = (index / questions.length * 100) + "%";
  $("compteur").textContent = `Question ${index + 1} / ${questions.length}  —  touche 1 à 5 possible`;
  $("question-libelle").textContent = q.question;
  const opts = $("options");
  opts.innerHTML = "";
  en_avance = false;
  if (q.type === "texte") {
    opts.classList.add("hidden");
    $("artiste-bloc").classList.remove("hidden");
    $("artiste-input").value = "";
    $("artiste-input").focus();
    return;
  }
  opts.classList.remove("hidden");
  $("artiste-bloc").classList.add("hidden");
  q.options.forEach((o, i) => {
    const b = document.createElement("button");
    b.className = "option";
    b.innerHTML = `<span class="touche">${i + 1}</span>${o.libelle}`;
    b.onclick = () => choisir(o.id, b);
    b.style.animationDelay = (i * 40) + "ms";
    opts.appendChild(b);
  });
}

function choisir(id, bouton) {
  if (en_avance) return;
  en_avance = true;
  reponses[questions[index].id] = id;
  if (bouton) bouton.classList.add("survol");
  index++;
  setTimeout(() => montrerQuestion(), 170);   // petit flash de confirmation
}

async function terminer() {
  if (en_avance) return;
  en_avance = true;
  const lecteur = $("lecteur");
  if (lecteur.src) { lecteur.pause(); lecteur.src = ""; }
  const artiste = ($("artiste-input").value || "").trim();
  $("quiz").classList.add("hidden");
  $("resultats").classList.add("hidden");
  $("chargement").classList.remove("hidden");
  $("tag-etape").textContent = "on fouille 24 styles pour toi…";
  try {
    const r = await fetch("/api/resultat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...reponses, artiste }),
    });
    if (!r.ok) throw new Error((await r.json()).detail || r.statusText);
    const d = await r.json();
    session_id = d.session_id;
    $("chargement").classList.add("hidden");
    afficherResultats(d);
  } catch (e) {
    $("chargement").classList.add("hidden");
    $("quiz").classList.remove("hidden");
    montrerQuestion();
    alert("La recherche n'a pas abouti : " + e.message);
  }
  en_avance = false;
}

function renderStyles(d) {
  const liste = d.styles || [];
  $("styles-gros").innerHTML = liste.map((s, i) => {
    const retour = session_id
      ? `<span class="react-style">
           <button class="style-retour oui" data-style="${s.cle}" data-action="aime">c'est moi</button>
           <button class="style-retour non" data-style="${s.cle}" data-action="pas">pas du tout</button>
         </span>`
      : "";
    return i === 0
      ? `<div class="style-xl bloc">${s.nom}${retour}</div>`
      : `<div class="style-l bloc">${s.nom}${retour}</div>`;
  }).join("");
  $("raisons").innerHTML = (d.raisons || []).map((r) =>
    `<li>${r}</li>`).join("");
  $("raisons").classList.toggle("hidden", !(d.raisons || []).length);
}

function afficherResultats(d) {
  $("resultats").classList.remove("hidden");
  renderStyles(d);
  renderPistes(d.pistes || []);
  $("tag-etape").textContent = "écoute en 30 s — 👍 pour en avoir d'autres proches";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderPistes(pistes) {
  const audio = $("lecteur");
  const en_cours = joue_cle_en_cours();
  $("pistes").innerHTML = pistes.map((p, i) => {
    const cle = p.artiste + " — " + p.titre;
    const joue_now = en_cours && cle === en_cours;
    return `
    <div class="piste entree${joue_now ? " joue" : ""}" style="animation-delay:${Math.min(i * 45, 450)}ms">
      <button class="play${joue_now ? " pause" : ""}" data-preview="${p.preview}" data-cle="${cle}" aria-label="écouter 30 s">${joue_now ? "❚❚" : "▶"}</button>
      <img class="pochette" src="${p.image}" loading="lazy" alt="">
      <div class="piste-info">
        <div class="piste-titre">${p.titre}</div>
        <div class="piste-artiste">${p.artiste} — ${p.album}</div>
        <div class="barre-preview${joue_now ? "" : " off"}"><span style="width:${joue_now ? barre_pct() : 0}%"></span></div>
      </div>
      <span class="piste-style">${p.style_nom || ""}</span>
      <a class="piste-lien" href="${p.lien}" target="_blank" rel="noopener">entier ↗</a>
      <button class="retour aime" data-artiste="${p.artiste}" data-titre="${p.titre}" data-style="${p.style_cle}">👍</button>
      <button class="retour pas" data-artiste="${p.artiste}" data-titre="${p.titre}" data-style="${p.style_cle}">👎</button>
    </div>`;
  }).join("");
}

function joue_cle_en_cours() {
  const audio = $("lecteur");
  return (audio.src && !audio.paused) ? (audio.dataset.cle || "") : "";
}

function barre_pct() {
  const audio = $("lecteur");
  return audio.duration ? Math.round(audio.currentTime / audio.duration * 100) : 0;
}

// ---------- lecture ----------
const audio = $("lecteur");
audio.addEventListener("timeupdate", () => {
  const barre = document.querySelector(".piste.joue .barre-preview span");
  if (barre && audio.duration) {
    barre.style.width = Math.round(audio.currentTime / audio.duration * 100) + "%";
  }
});
audio.addEventListener("ended", () => {
  document.querySelectorAll(".play").forEach((b) => b.textContent = "▶");
  document.querySelectorAll(".piste.joue").forEach((l) => {
    l.classList.remove("joue");
    const b = l.querySelector(".barre-preview span");
    if (b) b.style.width = "0%";
  });
  joue_cle = null;
});

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT") return;
  const q = questions[index];
  const n = parseInt(e.key, 10);
  if (q && q.options && n >= 1 && n <= q.options.length) {
    const boutons = document.querySelectorAll("#options .option");
    if (boutons[n - 1]) boutons[n - 1].click();
  }
});

document.addEventListener("click", async (e) => {
  const play = e.target.closest(".play");
  if (play) {
    if (audio.src === play.dataset.preview && !audio.paused) {
      audio.pause();
      play.textContent = "▶";
      document.querySelectorAll(".piste.joue").forEach((l) => l.classList.remove("joue"));
      return;
    }
    audio.pause();
    audio.src = play.dataset.preview;
    audio.dataset.cle = play.dataset.cle;
    audio.play();
    document.querySelectorAll(".play").forEach((b) => {
      b.textContent = "▶";
      b.classList.remove("pause");
    });
    document.querySelectorAll(".piste.joue").forEach((l) => {
      l.classList.remove("joue");
      const b = l.querySelector(".barre-preview span");
      if (b) b.style.width = "0%";
    });
    play.textContent = "❚❚";
    play.classList.add("pause");
    play.closest(".piste").classList.add("joue");
    return;
  }
  const retour_style = e.target.closest(".style-retour");
  if (retour_style && session_id) {
    retour_style.disabled = true;
    const r = await fetch("/api/retour", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id,
        style_cle: retour_style.dataset.style,
        action: retour_style.dataset.action,
      }),
    });
    const d = await r.json();
    renderStyles(d);
    renderPistes(d.pistes || []);
    toast(retour_style.dataset.action === "aime"
      ? "noté exact — on pousse plus fort vers ça"
      : "noté pas du tout — on décante ailleurs");
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
    renderStyles(d);
    renderPistes(d.pistes || []);     // le son continue : le lecteur est global
    toast(d.note || "raffiné d'après ton retour");
  }
});

function toast(texte) {
  const t = $("toast");
  t.textContent = texte;
  t.classList.add("visible");
  clearTimeout(t._chrono);
  t._chrono = setTimeout(() => t.classList.remove("visible"), 3200);
}

$("btn-fini").onclick = terminer;
$("artiste-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") terminer();
});
$("btn-recommencer").onclick = commencer;

commencer();
