
const quizForm = document.getElementById("quizForm");
const message = document.getElementById("message");
const submitBtn = document.getElementById("submitBtn");

quizForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!quizForm.reportValidity()) {
        return;
    }

    const answers = {};

    for (const [key, value] of new FormData(quizForm).entries()) {
        answers[key.substring(1)] = value;
    }

    submitBtn.disabled = true;
    message.textContent = "Submitting your quiz...";

    try {
        const response = await fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ answers })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Submission failed.");
        }

        // Display the automatically calculated score.
        message.textContent =
            `${result.message} Your score: ${result.score} out of ${result.total}.`;

        quizForm.querySelectorAll("input").forEach(input => {
            input.disabled = true;
        });

        submitBtn.textContent = "Quiz Submitted";
    } catch (error) {
        message.textContent = error.message;
        submitBtn.disabled = false;
    }
});
