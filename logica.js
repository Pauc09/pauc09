document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('encryptBtn').addEventListener('click', encryptText);
    document.getElementById('decryptBtn').addEventListener('click', decryptText);
    document.getElementById('copyBtn').addEventListener('click', copyText);

    // Agregar el evento 'input' al textarea para filtrar caracteres no deseados
    document.getElementById('inputText').addEventListener('input', filterInput);
});

function encryptText() {
    const inputText = document.getElementById('inputText').value;
    const encryptedText = inputText
        .replace(/e/g, 'enter')
        .replace(/i/g, 'imes')
        .replace(/a/g, 'ai')
        .replace(/o/g, 'ober')
        .replace(/u/g, 'ufat');
    document.getElementById('outputText').value = encryptedText;
}

function decryptText() {
    const inputText = document.getElementById('inputText').value;
    const decryptedText = inputText
        .replace(/enter/g, 'e')
        .replace(/imes/g, 'i')
        .replace(/ai/g, 'a')
        .replace(/ober/g, 'o')
        .replace(/ufat/g, 'u');
    document.getElementById('outputText').value = decryptedText;
}

function copyText() {
    const outputText = document.getElementById('outputText');
    outputText.select();
    document.execCommand('copy');
    alert('Texto copiado al portapapeles');
}

function filterInput(event) {
    const inputText = document.getElementById('inputText');
    let inputValue = inputText.value;

    // Definir un patrón para permitir solo caracteres válidos (letras y números)
    const validPattern = /^[a-zA-Z0-9\s]*$/;

    // Filtrar caracteres no deseados
    if (!validPattern.test(inputValue)) {
        inputText.value = inputValue.replace(/[^a-zA-Z0-9\s]/g, '');
    }
}
