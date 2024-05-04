function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {
    // Si le scan est réussi
    function onScanSuccess(decodeText, decodeResult) {
        fetch('/dashboard?numero_unique=' + decodeText)
            .then(response => response.text()) // Convertit la réponse en texte
            .then(data => {
                // Vérifie si le message d'erreur indiquant qu'aucun patient n'est trouvé
                if (data.includes('Aucun patient trouvé avec ce numéro unique.')) {
                    alert('Aucun patient n\'est identifié par ce QR code.');
                } else {
                    // Si aucun message d'erreur, redirigez l'utilisateur vers la page fiche_patient.html
                    window.location.href = "/fiche_patient?numero_unique=" + decodeText;
                }
            })
            .catch(error => console.error('Erreur:', error));
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});