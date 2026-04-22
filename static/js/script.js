document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('tripForm');
    const button = document.getElementById('generateBtn');

    // Disable button on submit
    if (form && button) {
        form.addEventListener('submit', function () {
            button.disabled = true;
            button.textContent = 'Generating...';
        });
    }

    // Bootstrap tooltips
    const tooltipTriggers = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggers.length && window.bootstrap) {
        tooltipTriggers.map(function (trigger) {
            return new bootstrap.Tooltip(trigger);
        });
    }

    // Copy itinerary
    const copyButtons = document.querySelectorAll('.copy-itinerary');
    copyButtons.forEach(function (copyButton) {
        copyButton.addEventListener('click', function () {
            const target = document.querySelector(copyButton.dataset.copyTarget);
            if (!target) return;

            navigator.clipboard.writeText(target.textContent.trim()).then(function () {
                const originalText = copyButton.textContent;
                copyButton.textContent = 'Copied!';
                setTimeout(function () {
                    copyButton.textContent = originalText;
                }, 1500);
            });
        });
    });

    // 🔥 FIX: Always show content (no animation dependency)
    const reveals = document.querySelectorAll('.content-reveal');
    reveals.forEach(function (section) {
        section.classList.add('is-visible');
    });
});
