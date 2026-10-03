document.addEventListener("DOMContentLoaded", function () {
    var fitnessForm = document.getElementById("fitnessForm");
    if (fitnessForm) {
        fitnessForm.addEventListener("submit", function () {
            var btn = document.getElementById("submitBtn");
            if (btn) {
                btn.querySelector(".btn-text").style.display = "none";
                btn.querySelector(".btn-loading").style.display = "inline";
                btn.disabled = true;
            }
        });
    }
    var feedbackForm = document.getElementById("feedbackForm");
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function () {
            var btn = document.getElementById("feedbackBtn");
            if (btn) {
                btn.querySelector(".btn-text").style.display = "none";
                btn.querySelector(".btn-loading").style.display = "inline";
                btn.disabled = true;
            }
        });
    }
});
