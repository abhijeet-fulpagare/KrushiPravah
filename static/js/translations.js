const translations = {
    // Navigation
    'Home': 'मुख्यपृष्ठ',
    'Price Prediction': 'किंमत भाकीत',
    'Price Trends': 'किंमत ट्रेंड्स',
    'Demand and Supply': 'मागणी आणि पुरवठा',
    'Change to Marathi': 'मराठीमध्ये बदला',
    'Change to English': 'इंग्रजीमध्ये बदला',

    // Common
    'Select Market': 'बाजार निवडा',
    'Select Vegetable': 'भाजी निवडा',
    'Choose a vegetable...': 'भाजी निवडा...',
    'Get Price Prediction': 'किंमत भाकीत मिळवा',
    'Select Date': 'तारीख निवडा',
    'Current Price': 'सध्याची किंमत',
    'Minimum Price': 'किमान किंमत',
    'Maximum Price': 'कमाल किंमत',
    'per Quintal': 'प्रति क्विंटल',
    'Price Trends': 'किंमत ट्रेंड्स',
    'Track vegetable price changes over time': 'कालांतराने भाज्यांच्या किमतीतील बदल ट्रॅक करा',
    'Select Time Range': 'कालावधी निवडा',
    'Last 7 Days': 'मागील 7 दिवस',
    'Last 2 Weeks': 'मागील 2 आठवडे',
    'Last Month': 'मागील महिना',
    'Last 2 Months': 'मागील 2 महिने',
    'All Time': 'सर्व काळ',
    'Current Price Details': 'सध्याच्या किमतीचा तपशील',
    'Available Quantity': 'उपलब्ध प्रमाण',
    'Quintal': 'क्विंटल',
    'Price (₹/Quintal)': 'किंमत (₹/क्विंटल)',
    'Date': 'तारीख',

    // Index page
    'Maharashtra Vegetable Price Analyzer': 'महाराष्ट्र भाजीपाला किंमत विश्लेषक',
    "Today's Market Prices": 'आजच्या बाजारातील किंमती',
    "Today's Top Vegetables": 'आजच्या टॉप भाज्या',
    'Pune Market': 'पुणे बाजार',
    'from last week': 'मागील आठवड्यापासून',

    // Price prediction page
    'Price Prediction': 'किंमत भाकीत',
    'Predict vegetable prices for future dates': 'भविष्यातील तारखांसाठी भाज्यांच्या किमतींचे भाकीत करा',

    // Error messages
    'Please select both vegetable and date': 'कृपया भाजी आणि तारीख दोन्ही निवडा',
    'An error occurred while fetching the prediction': 'भाकीत आणताना त्रुटी आली',
    'No prediction found for': 'साठी भाकीत सापडले नाही',
    'Available dates:': 'उपलब्ध तारखा:',
    'Failed to load price trends': 'किंमत ट्रेंड लोड करण्यात अयशस्वी',
    'Please try again': 'कृपया पुन्हा प्रयत्न करा',
    'Please select a vegetable': 'कृपया भाजी निवडा'
};

// Reverse translations (Marathi to English)
const reverseTranslations = {};
for (const [english, marathi] of Object.entries(translations)) {
    reverseTranslations[marathi] = english;
} 