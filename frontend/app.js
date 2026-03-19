document.getElementById('imageInput').addEventListener('change', function(e) {
    const fileName = e.target.files[0] ? e.target.files[0].name : 'Importer une photo (Optionnel)';
    document.getElementById('fileName').textContent = fileName;
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const textInput = document.getElementById('foodInput').value.trim();
    const fileInput = document.getElementById('imageInput').files[0];

    if (!textInput && !fileInput) {
        alert("Veuillez saisir un texte ou sélectionner une image.");
        return;
    }

    const payload = { text_query: textInput };

    if (fileInput) {
        const reader = new FileReader();
        reader.readAsDataURL(fileInput);
        reader.onload = async () => {
            payload.image_data = reader.result;
            await sendRequest(payload);
        };
        reader.onerror = error => console.error("Error reading file:", error);
    } else {
        await sendRequest(payload);
    }
});

async function sendRequest(payload) {
    const btn = document.getElementById('analyzeBtn');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('resultCard');

    btn.disabled = true;
    loader.classList.remove('hidden');
    resultCard.classList.add('hidden');

    try {
        const response = await fetch('/api/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || "Erreur serveur");
        }
        
        const data = await response.json();
        displayResult(data);
    } catch (err) {
        alert(err.message);
    } finally {
        btn.disabled = false;
        loader.classList.add('hidden');
    }
}

function displayResult(data) {
    const resultCard = document.getElementById('resultCard');
    const foodName = document.getElementById('foodName');
    const scoreBar = document.getElementById('scoreBar');
    const scoreValue = document.getElementById('scoreValue');
    const badge = document.getElementById('classificationBadge');
    const advice = document.getElementById('adviceText');
    const followupCont = document.getElementById('followupContainer');
    const followupQ = document.getElementById('followupQuestion');

    // Reset styles
    badge.className = 'classification-badge';
    
    // Fill data
    foodName.textContent = data.food_name || "Résultat";
    advice.textContent = data.advice || "";
    
    let color = "#ffffff";
    let width = "0%";
    let badgeClass = "badge-unknown";

    if (data.status === "needs_info") {
        followupCont.classList.remove('hidden');
        followupQ.textContent = data.followup_question || "Pouvez-vous préciser ?";
        scoreValue.textContent = "?/5";
    } else {
        followupCont.classList.add('hidden');
        if (data.visual_score) {
            scoreValue.textContent = `${data.visual_score}/5`;
            width = `${(data.visual_score / 5) * 100}%`;
            
            if (data.visual_score <= 2) { color = "var(--score-1)"; badgeClass = "badge-avoid"; }
            else if (data.visual_score === 3) { color = "var(--score-3)"; badgeClass = "badge-mod"; }
            else { color = "var(--score-5)"; badgeClass = "badge-priv"; }
        }
    }

    badge.classList.add(badgeClass);
    badge.textContent = data.classification === "inconnu" ? "INCONNU" : data.classification.toUpperCase();
    
    resultCard.classList.remove('hidden');
    
    // Animate score bar slightly after render
    setTimeout(() => {
        scoreBar.style.width = width;
        scoreBar.style.backgroundColor = color;
    }, 100);
}
