// ===== DOM Elements =====
const sourceTextArea = document.getElementById('source-text');
const targetTextDiv = document.getElementById('target-text');
const sourceLangSelect = document.getElementById('source-lang');
const targetLangSelect = document.getElementById('target-lang');
const modelSelect = document.getElementById('model-select');
const modelNameFooter = document.getElementById('model-name-footer');
const swapBtn = document.getElementById('swap-btn');
const translateBtn = document.getElementById('translate-btn');
const clearBtn = document.getElementById('clear-btn');
const copyBtn = document.getElementById('copy-btn');
const charCount = document.getElementById('char-count');
const loadingIndicator = document.getElementById('loading');
const toast = document.getElementById('toast');

const MAX_CHARS = 5000;
let isTranslating = false;
let debounceTimer = null;
let currentModels = [];

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([loadLanguages(), loadModels()]);
    setupEventListeners();

    // Set default languages
    sourceLangSelect.value = 'en';
    targetLangSelect.value = 'zh-Hant';
});

// ===== Load Languages =====
async function loadLanguages() {
    try {
        const response = await fetch('/api/languages');
        const data = await response.json();

        const languages = data.languages;

        languages.forEach(lang => {
            const optionSource = document.createElement('option');
            optionSource.value = lang.code;
            optionSource.textContent = `${lang.nativeName} (${lang.name})`;
            sourceLangSelect.appendChild(optionSource);

            const optionTarget = document.createElement('option');
            optionTarget.value = lang.code;
            optionTarget.textContent = `${lang.nativeName} (${lang.name})`;
            targetLangSelect.appendChild(optionTarget);
        });
    } catch (error) {
        console.error('Failed to load languages:', error);
        showToast('無法載入語言列表');
    }
}

// ===== Load Models =====
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        currentModels = data.models;

        modelSelect.innerHTML = '';
        currentModels.forEach(model => {
            const option = document.createElement('option');
            option.value = model.id;
            if (model.installed) {
                option.textContent = `${model.name} (${model.size}) - ${model.description}`;
            } else {
                option.textContent = `${model.name} (${model.size}) - 未安裝`;
                option.disabled = true;
            }
            modelSelect.appendChild(option);
        });

        // Select first installed model
        const firstInstalled = currentModels.find(m => m.installed);
        if (firstInstalled) {
            modelSelect.value = firstInstalled.id;
            updateFooterModelName(firstInstalled.name);
        }
    } catch (error) {
        console.error('Failed to load models:', error);
        // Fallback
        const option = document.createElement('option');
        option.value = 'translategemma:4b';
        option.textContent = 'TranslateGemma 4B (3.3 GB)';
        modelSelect.appendChild(option);
    }
}

// ===== Update Footer Model Name =====
function updateFooterModelName(name) {
    if (modelNameFooter) {
        modelNameFooter.textContent = name;
    }
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Translate button
    translateBtn.addEventListener('click', translate);

    // Source text input
    sourceTextArea.addEventListener('input', () => {
        updateCharCount();
        // Auto-translate with debounce (optional - disabled by default)
        // debouncedTranslate();
    });

    // Keyboard shortcut: Ctrl/Cmd + Enter to translate
    sourceTextArea.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            translate();
        }
    });

    // Swap languages
    swapBtn.addEventListener('click', swapLanguages);

    // Clear button
    clearBtn.addEventListener('click', clearSource);

    // Copy button
    copyBtn.addEventListener('click', copyTranslation);

    // Model selection change
    modelSelect.addEventListener('change', () => {
        const selectedModel = currentModels.find(m => m.id === modelSelect.value);
        if (selectedModel) {
            updateFooterModelName(selectedModel.name);
            showToast(`已切換至 ${selectedModel.name}`);
        }
    });
}

// ===== Translation =====
async function translate() {
    const text = sourceTextArea.value.trim();

    if (!text) {
        targetTextDiv.innerHTML = '<span class="placeholder-text">翻譯結果將顯示在這裡...</span>';
        return;
    }

    if (isTranslating) return;

    isTranslating = true;
    translateBtn.disabled = true;
    loadingIndicator.classList.add('active');
    targetTextDiv.innerHTML = '';

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLangSelect.value,
                target_lang: targetLangSelect.value,
                model: modelSelect.value,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '翻譯失敗');
        }

        const data = await response.json();
        targetTextDiv.textContent = data.translated_text;

    } catch (error) {
        console.error('Translation error:', error);
        targetTextDiv.innerHTML = `<span style="color: #ef4444;">錯誤: ${error.message}</span>`;
        showToast('翻譯失敗，請稍後再試');
    } finally {
        isTranslating = false;
        translateBtn.disabled = false;
        loadingIndicator.classList.remove('active');
    }
}

// ===== Debounced Translate (for auto-translate feature) =====
function debouncedTranslate() {
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    debounceTimer = setTimeout(() => {
        translate();
    }, 500);
}

// ===== Swap Languages =====
function swapLanguages() {
    // Swap language selections
    const tempLang = sourceLangSelect.value;
    sourceLangSelect.value = targetLangSelect.value;
    targetLangSelect.value = tempLang;

    // Swap text content
    const translatedText = targetTextDiv.textContent;
    if (translatedText && !targetTextDiv.querySelector('.placeholder-text')) {
        sourceTextArea.value = translatedText;
        targetTextDiv.innerHTML = '<span class="placeholder-text">翻譯結果將顯示在這裡...</span>';
        updateCharCount();
    }
}

// ===== Clear Source =====
function clearSource() {
    sourceTextArea.value = '';
    targetTextDiv.innerHTML = '<span class="placeholder-text">翻譯結果將顯示在這裡...</span>';
    updateCharCount();
    sourceTextArea.focus();
}

// ===== Copy Translation =====
async function copyTranslation() {
    const text = targetTextDiv.textContent;

    if (!text || targetTextDiv.querySelector('.placeholder-text')) {
        showToast('沒有可複製的內容');
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        showToast('已複製到剪貼簿');
    } catch (error) {
        console.error('Copy failed:', error);
        showToast('複製失敗');
    }
}

// ===== Update Character Count =====
function updateCharCount() {
    const count = sourceTextArea.value.length;
    charCount.textContent = `${count} / ${MAX_CHARS}`;

    if (count > MAX_CHARS) {
        charCount.style.color = '#ef4444';
        sourceTextArea.value = sourceTextArea.value.substring(0, MAX_CHARS);
        charCount.textContent = `${MAX_CHARS} / ${MAX_CHARS}`;
    } else if (count > MAX_CHARS * 0.9) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '';
    }
}

// ===== Show Toast =====
function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2500);
}
