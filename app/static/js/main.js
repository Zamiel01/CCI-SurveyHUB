// CCI SurveyHUB - Main JS
console.log('SurveyHUB loaded');

/**
 * Triggers the themed loading animation overlay.
 * @param {string} title - Core header message (e.g., 'Validating Schema')
 * @param {string} subtitle - Secondary action hint (e.g., 'Analyzing SIRET numbers...')
 */
function showSurveyLoader(title = "SurveyHUB Data Nexus", subtitle = "Processing request...") {
    document.getElementById('spinner-title').innerText = title;
    document.getElementById('spinner-text').innerText = subtitle;
    document.getElementById('global-spinner').classList.remove('d-none');
}

/**
 * Dismisses the active loading overlay.
 */
function hideSurveyLoader() {
    document.getElementById('global-spinner').classList.add('d-none');
}

// Quick developer test route check (Runs loop inside your console log setup)
// Open browser inspect panel, type: showSurveyLoader("Export Engine Active", "Parsing with Pandas...")
