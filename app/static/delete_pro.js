// Sélectionnez le bouton "Modifier"
const modifierButton = document.getElementById('modifyButton');

// Sélectionnez les cases à cocher et le bouton "Supprimer"
const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const deleteButton = document.querySelector('button[type="submit"]');

// Initialisez les cases à cocher et le bouton "Supprimer" comme cachés
checkboxes.forEach(checkbox => checkbox.style.display = 'none');
deleteButton.style.display = 'none';

// Ajoutez un gestionnaire d'événements pour le clic sur le bouton "Modifier"
modifierButton.addEventListener('click', () => {
    // Affichez ou masquez les cases à cocher et le bouton "Supprimer" en fonction de leur état actuel
    if (deleteButton.style.display === 'none') {
        checkboxes.forEach(checkbox => checkbox.style.display = 'block');
        deleteButton.style.display = 'block';
    } else {
        checkboxes.forEach(checkbox => checkbox.style.display = 'none');
        deleteButton.style.display = 'none';
    }
});

// Ajoutez un gestionnaire d'événements pour le clic sur le bouton "Supprimer"
document.querySelectorAll('.button').forEach(button => button.addEventListener('click', e => {
    // Si le bouton n'a pas déjà la classe 'delete', ajoutez-la et planifiez son retrait après 5 secondes
    if (!button.classList.contains('delete')) {
        button.classList.add('delete');
        setTimeout(() => {
            button.classList.remove('delete');
            document.getElementById('selectedProIds').value = getSelectedProIds();
            document.getElementById('deleteForm').submit(); // Soumettre le formulaire
        }, 5000);
    }
    e.preventDefault();
}));

// Fonction pour obtenir les ID des Pros sélectionnés
function getSelectedProIds() {
    const selectedIds = [];
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedIds.push(checkbox.value);
        }
    });
    return selectedIds.join(',');
}