document.addEventListener('DOMContentLoaded', () => {
    const languageSelector = document.getElementById('language-selector');
    const savedLanguage = localStorage.getItem('language') || 'en';
    languageSelector.value = savedLanguage;
    languageSelector.addEventListener('change', () => {
        const selectedLanguage = languageSelector.value;
        localStorage.setItem('language', selectedLanguage);
        updateLanguage(selectedLanguage);
    });
    updateLanguage(savedLanguage); // Set initial language based on saved preference
});

function updateLanguage(language) {
    console.log(`Updating language to: ${language}`);
    fetch(`/static/locales/${language}.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error fetching translation file: ${response.statusText}`);
            }
            return response.json();
        })
        .then(translation => {
            console.log('Translation fetched:', translation);
            applyTranslations(translation);
        })
        .catch(error => console.error('Error:', error));
}

function applyTranslations(translation) {
    document.getElementById('username').placeholder = translation.username;
    document.getElementById('password').placeholder = translation.password;
    document.querySelector('.submit-image').alt = translation.submit;

    // Log to verify the changes
    console.log('Applied translations:', translation);
}
