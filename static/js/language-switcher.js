let currentLanguage = localStorage.getItem('language') || 'mr';

function translateElement(element) {
    // Check for data-translate attribute first
    const translateKey = element.getAttribute('data-translate');
    if (translateKey && translations[currentLanguage][translateKey]) {
        element.textContent = translations[currentLanguage][translateKey];
        return;
    }

    // Fall back to direct text translation if no data-translate attribute
    const text = element.textContent.trim();
    if (currentLanguage === 'en') {
        // Translating from Marathi to English
        if (reverseTranslations[text]) {
            element.textContent = reverseTranslations[text];
        }
    } else {
        // Translating from English to Marathi
        if (translations['mr'][text]) {
            element.textContent = translations['mr'][text];
        }
    }
    
    // Handle placeholders for inputs
    if (element.placeholder) {
        const placeholderText = element.placeholder.trim();
        if (currentLanguage === 'en' && reverseTranslations[placeholderText]) {
            element.placeholder = reverseTranslations[placeholderText];
        } else if (translations['mr'][placeholderText]) {
            element.placeholder = translations['mr'][placeholderText];
        }
    }
}

function translatePage() {
    // Translate all elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(translateElement);

    // Translate navigation links
    document.querySelectorAll('.nav-link').forEach(translateElement);

    // Translate headings
    document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(translateElement);

    // Translate paragraphs
    document.querySelectorAll('p').forEach(translateElement);

    // Translate labels
    document.querySelectorAll('label').forEach(translateElement);

    // Translate buttons (except language button)
    document.querySelectorAll('button:not(.language-btn)').forEach(translateElement);

    // Translate select options
    document.querySelectorAll('option').forEach(translateElement);

    // Translate spans
    document.querySelectorAll('span').forEach(translateElement);

    // Translate div elements with direct text
    document.querySelectorAll('div').forEach(element => {
        if (element.childNodes.length === 1 && element.childNodes[0].nodeType === Node.TEXT_NODE) {
            translateElement(element);
        }
    });

    // Update language button text
    const languageBtn = document.querySelector('.language-btn');
    if (languageBtn) {
        languageBtn.textContent = currentLanguage === 'en' ? 'मराठी मध्ये बदला' : 'Switch to English';
    }

    // Update html lang attribute
    document.documentElement.lang = currentLanguage;
}

// Initialize language switcher
document.addEventListener('DOMContentLoaded', function() {
    // Initial translation
    translatePage();
    
    // Language switch button click handler
    document.querySelector('.language-btn').addEventListener('click', function() {
        currentLanguage = currentLanguage === 'en' ? 'mr' : 'en';
        localStorage.setItem('language', currentLanguage);
        translatePage();
    });
}); 