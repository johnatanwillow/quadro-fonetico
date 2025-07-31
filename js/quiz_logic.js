// O script de quiz e resultados será combinado em um único arquivo para simplificar.

// --- BANCO DE PALAVRAS ---
// O banco de dados completo de 100 palavras do inglês e do francês
const QUIZ_WORDS_EN = [
    "phone", "book", "house", "chair", "water", "mouse", "key", "table", "orange", "friend",
    "apple", "banana", "grape", "lemon", "strawberry", "cookie", "cake", "bread", "milk", "cheese",
    "sugar", "salt", "meat", "fish", "vegetable", "fruit", "pencil", "eraser", "notebook", "pen",
    "paper", "school", "teacher", "student", "class", "history", "geography", "mathematics", "science", "music",
    "sport", "english", "french", "spanish", "german", "friendship", "family", "father", "mother", "brother",
    "sister", "grandfather", "grandmother", "uncle", "aunt", "cousin", "dog", "cat", "bird", "fish",
    "flower", "tree", "sun", "moon", "star", "sky", "sea", "river", "mountain", "forest",
    "city", "village", "street", "square", "restaurant", "cafe", "hotel", "station", "airport", "train",
    "plane", "bus", "bicycle", "foot", "hand", "head", "arm", "leg", "body", "heart",
    "stomach", "phone call", "computer science", "history book", "music class"
];

const QUIZ_WORDS_FR = [
    "fenêtre", "maison", "voiture", "livre", "ordinateur", "jour", "nuit", "porte", "tête", "main",
    "table", "chaise", "lit", "lampe", "téléphone", "stylo", "papier", "crayon", "gomme", "cahier",
    "école", "professeur", "étudiant", "classe", "histoire", "géographie", "mathématiques", "science", "sport", "musique",
    "français", "anglais", "espagnol", "allemand", "ami", "famille", "père", "mère", "frère", "sœur",
    "grand-père", "grand-mère", "oncle", "tante", "cousin", "cousine", "chien", "chat", "oiseau", "poisson",
    "fleur", "arbre", "soleil", "lune", "étoile", "ciel", "mer", "rivière", "montagne", "forêt",
    "ville", "village", "rue", "place", "restaurant", "café", "hôtel", "gare", "aéroport", "train",
    "avion", "bus", "vélo", "pied", "main", "tête", "bras", "jambe", "corps", "cœur",
    "estomac", "eau", "lait", "fromage", "pain", "beurre", "sucre", "sel", "viande", "poisson",
    "fruit", "légume", "pomme", "orange", "banane", "fraise", "chocolat", "gâteau"
];

// --- LÓGICA DO QUIZ ---
if (document.getElementById('quiz-content')) {
    let currentQuestionIndex = 0;
    let score = 0;
    const quizLength = 10;
    let language = 'en';
    let quizQuestions = [];
    const audioPlayer = new Audio();

    // Referências aos elementos HTML
    const playSoundButton = document.getElementById('play-sound-button');
    const optionsGrid = document.getElementById('options-grid');
    const nextButton = document.getElementById('next-button');
    const questionCounter = document.getElementById('question-counter');
    const quizContent = document.getElementById('quiz-content');

    // Funções auxiliares
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    function generateQuizQuestions(wordList) {
        // Garantindo que a lista tenha pelo menos 4 palavras para não quebrar a lógica dos distratores
        if (wordList.length < 4) {
            console.error("Erro: A lista de palavras é muito pequena para gerar um questionário.");
            return [];
        }

        shuffleArray(wordList);
        const selectedWords = wordList.slice(0, quizLength);

        return selectedWords.map(correctWord => {
            // Remove a palavra correta da lista de distratores
            const availableDistractors = wordList.filter(word => word !== correctWord);
            shuffleArray(availableDistractors);

            // Seleciona 3 distratores
            const distractors = availableDistractors.slice(0, 3);
            
            const options = [...distractors, correctWord];
            shuffleArray(options);

            const correctAnswerIndex = options.indexOf(correctWord);

            return {
                audioSrc: `audio/${language === 'en' ? 'quiz_en_' : 'quiz_fr_'}${correctWord.replace(/ /g, '_')}.mp3`,
                options: options,
                correctAnswerIndex: correctAnswerIndex,
                correctWord: correctWord
            };
        });
    }

    function loadQuestion() {
        if (currentQuestionIndex >= quizQuestions.length) {
            // Fim do quiz: salva o estado completo no localStorage e redireciona
            localStorage.setItem('quizQuestions', JSON.stringify(quizQuestions));
            localStorage.setItem('quizScore', score);
            localStorage.setItem('quizTotal', quizQuestions.length);
            window.location.href = `results.html?lang=${language}`;
            return;
        }

        const question = quizQuestions[currentQuestionIndex];
        optionsGrid.innerHTML = '';
        
        // Atualiza o contador de perguntas
        questionCounter.textContent = `${currentQuestionIndex + 1} de ${quizLength}`;

        // Cria os botões de opção
        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.classList.add('phoneme-button');
            button.innerHTML = `<span>${option}</span>`;
            button.onclick = () => checkAnswer(index);
            optionsGrid.appendChild(button);
        });

        // Configura o reprodutor de áudio
        audioPlayer.src = question.audioSrc;
        
        // Reseta o estado dos botões
        nextButton.style.display = 'none';
        nextButton.textContent = 'Próxima Pergunta';
        playSoundButton.style.display = 'block';
        playSoundButton.disabled = false;
        
        // Toca o áudio automaticamente após carregar a pergunta
        audioPlayer.play().catch(e => console.error("Erro ao reproduzir áudio:", e));

        document.querySelectorAll('.phoneme-button').forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('correct', 'incorrect');
        });
    }

    function checkAnswer(selectedIndex) {
        const question = quizQuestions[currentQuestionIndex];
        const buttons = optionsGrid.querySelectorAll('.phoneme-button');
        
        // Salva a resposta do usuário no objeto da pergunta
        question.userAnswerIndex = selectedIndex;

        // Desabilita os botões de opção após a escolha
        buttons.forEach(btn => btn.disabled = true);
        playSoundButton.disabled = true;

        if (selectedIndex === question.correctAnswerIndex) {
            buttons[selectedIndex].classList.add('correct');
            score++;
        } else {
            buttons[selectedIndex].classList.add('incorrect');
            buttons[question.correctAnswerIndex].classList.add('correct');
        }
        
        nextButton.style.display = 'block';
    }

    // Event listeners
    playSoundButton.onclick = () => {
        audioPlayer.play().catch(e => console.error("Erro ao reproduzir áudio:", e));
    };

    nextButton.onclick = () => {
        currentQuestionIndex++;
        loadQuestion();
    };

    // Inicia o quiz ao carregar a página
    window.addEventListener('load', () => {
        const urlParams = new URLSearchParams(window.location.search);
        language = urlParams.get('lang') || 'en';

        // Determina a lista de palavras com base no idioma
        const wordList = language === 'en' ? QUIZ_WORDS_EN : QUIZ_WORDS_FR;
        quizQuestions = generateQuizQuestions(wordList);
        
        if (quizQuestions.length > 0) {
            loadQuestion();
        } else {
            quizContent.innerHTML = "<p>Ocorreu um erro ao carregar o questionário. Verifique se o banco de palavras está completo.</p>";
        }
    });
}


// --- LÓGICA DE RESULTADOS E RANKING ---
if (document.getElementById('ranking-table-body')) {
    const urlParams = new URLSearchParams(window.location.search);
    const language = urlParams.get('lang') || 'en';
    const quizQuestions = JSON.parse(localStorage.getItem('quizQuestions')) || [];
    const finalScore = parseInt(localStorage.getItem('quizScore')) || 0;
    const totalQuestions = parseInt(localStorage.getItem('quizTotal')) || 0;
    
    // Referências aos elementos HTML
    const finalScoreDisplay = document.getElementById('final-score-display');
    const languageDisplay = document.getElementById('language-display');
    const reviewList = document.getElementById('review-list');
    const rankingForm = document.getElementById('ranking-form');
    const rankingTableBody = document.getElementById('ranking-table-body');
    
    // Mostra a pontuação final
    finalScoreDisplay.textContent = `${finalScore}/${totalQuestions}`;
    languageDisplay.textContent = language === 'en' ? 'Inglês' : 'Francês';

    // Gera a revisão das perguntas
    if (quizQuestions.length > 0) {
        quizQuestions.forEach((question, index) => {
            const reviewItem = document.createElement('li');
            const isCorrect = question.userAnswerIndex === question.correctAnswerIndex;
            reviewItem.classList.add('review-item', isCorrect ? 'correct' : 'incorrect');

            reviewItem.innerHTML = `
                <div class="review-question-info">
                    <p><strong>Questão ${index + 1}:</strong></p>
                    <button class="review-audio-button" data-audio-src="${question.audioSrc}">Ouvir Som</button>
                    <p>Sua resposta: <span class="answer-text">${question.options[question.userAnswerIndex]}</span></p>
                    <p>Resposta correta: <span class="correct-text">${question.options[question.correctAnswerIndex]}</span></p>
                </div>
            `;
            reviewList.appendChild(reviewItem);
        });

        // Adiciona event listeners para os botões de áudio de revisão
        document.querySelectorAll('.review-audio-button').forEach(button => {
            button.addEventListener('click', (event) => {
                const audio = new Audio(event.currentTarget.dataset.audioSrc);
                audio.play().catch(e => console.error("Erro ao reproduzir áudio:", e));
            });
        });
    }

    // --- Lógica de Ranking ---
    const getRankingKey = () => `quizRanking_${language}`;

    rankingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const playerName = document.getElementById('player-name').value || 'Anônimo';
        
        const rankingKey = getRankingKey();
        let ranking = JSON.parse(localStorage.getItem(rankingKey)) || [];
        
        ranking.push({ name: playerName, score: finalScore, total: totalQuestions });
        ranking.sort((a, b) => b.score - a.score); // Ordena por pontuação
        ranking = ranking.slice(0, 10); // Mantém apenas os 10 melhores
        
        localStorage.setItem(rankingKey, JSON.stringify(ranking));
        displayRanking(ranking);
        rankingForm.style.display = 'none'; // Esconde o formulário após enviar
    });
    
    function displayRanking(ranking) {
        rankingTableBody.innerHTML = '';
        ranking.forEach((entry, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${entry.name}</td>
                <td>${entry.score}/${entry.total}</td>
            `;
            rankingTableBody.appendChild(row);
        });
    }

    const rankingKey = getRankingKey();
    const currentRanking = JSON.parse(localStorage.getItem(rankingKey)) || [];
    displayRanking(currentRanking);
}