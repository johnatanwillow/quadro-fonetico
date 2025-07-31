const currentAudio = new Audio();

function playAudio(event) {
    const button = event.currentTarget;
    const audioSrc = button.dataset.audio;

    if (!currentAudio.paused) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    currentAudio.src = audioSrc;
    currentAudio.play().catch(e => {
        console.error("Erro ao reproduzir áudio:", e);
        alert("Ops! Não foi possível tocar o som. 🙁 Verifique se os arquivos de áudio estão na pasta 'audio' e se os nomes dos arquivos estão corretos!");
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const allPhonemeButtons = document.querySelectorAll('.phoneme-button, .word-button');
    allPhonemeButtons.forEach(button => {
        button.addEventListener('click', playAudio);
    });
});