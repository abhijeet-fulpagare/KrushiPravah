let currentLanguage = 'en';

function translateElement(element) {
    const text = element.textContent.trim();
    const translationMap = currentLanguage === 'en' ? translations : reverseTranslations;
    
    if (translationMap[text]) {
        element.textContent = translationMap[text];
    }
    
    // Handle placeholders for inputs
    if (element.placeholder && translationMap[element.placeholder]) {
        element.placeholder = translationMap[element.placeholder];
    }
}

function translatePage() {
    // Update language button text - show opposite language option
    const languageBtn = document.querySelector('.language-btn');
    if (languageBtn) {
        // When in English mode, show Marathi text
        // When in Marathi mode, show Marathi text for English
        languageBtn.textContent = currentLanguage === 'en' ? 'Change to English' : 'मराठी मध्ये बदला';
    }

    // Translate navigation links
    document.querySelectorAll('.nav-link').forEach(translateElement);

    // Translate headings
    document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(translateElement);

    // Translate paragraphs
    document.querySelectorAll('p').forEach(translateElement);

    // Translate labels
    document.querySelectorAll('label').forEach(translateElement);

    // Translate buttons:not(.language-btn)
    document.querySelectorAll('button:not(.language-btn)').forEach(translateElement);

    // Translate select options
    document.querySelectorAll('option').forEach(translateElement);

    // Translate spans with text
    document.querySelectorAll('span').forEach(translateElement);

    // Translate div elements with direct text
    document.querySelectorAll('div').forEach(element => {
        if (element.childNodes.length === 1 && element.childNodes[0].nodeType === Node.TEXT_NODE) {
            translateElement(element);
        }
    });
}

function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'mr' : 'en';
    translatePage();
    
    // Store language preference
    localStorage.setItem('preferredLanguage', currentLanguage);
}

// Initialize language switcher
document.addEventListener('DOMContentLoaded', () => {
    // Load saved language preference
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
        currentLanguage = savedLanguage;
        translatePage();
    } else {
        // Set initial button text to Marathi since default is English
        const languageBtn = document.querySelector('.language-btn');
        if (languageBtn) {
            languageBtn.textContent = 'मराठी मध्ये बदला';
        }
    }

    // Add click event to language button
    const languageBtn = document.querySelector('.language-btn');
    if (languageBtn) {
        languageBtn.addEventListener('click', toggleLanguage);
    }
}); 