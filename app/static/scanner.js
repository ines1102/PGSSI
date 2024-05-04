// script.js file

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

    // If found your qr code
    function onScanSuccess(decodeText, decodeResult) {
        fetch('/dashboard?numero_unique=' + decodeText)
            .then(response => response.text()) // Convertit la réponse en texte
            .then(data => {
                if (data.error) {
                    alert(data.error); // Affiche le message d'erreur dans une popup
                } else {
                    // Si aucun message d'erreur, affichez les informations du patient
                    document.getElementById('dashboard').innerText = data;
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
