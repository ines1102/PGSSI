// email.js

// Initialiser EmailJS avec votre Service ID
emailjs.init("service_2qidfyd");

// Fonction pour envoyer un e-mail temporaire contenant le mot de passe temporaire
function sendTemporaryPassword(email, temporaryPassword) {
    // Envoyer l'e-mail avec EmailJS
    emailjs.send("service_2qidfyd", "template_4g3bca9", {
        to_name: email, // Remplacez "John" par l'adresse e-mail du destinataire
        message: `Bonjour, voici votre mot de passe temporaire : ${temporaryPassword}`
    })
        .then(function (response) {
            console.log("E-mail envoyé avec succès !", response);
        }, function (error) {
            console.error("Erreur lors de l'envoi de l'e-mail :", error);
        });
}
