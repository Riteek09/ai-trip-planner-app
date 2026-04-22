document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('tripForm');
    const button = document.getElementById('generateBtn');
    const tooltipTriggers = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

    if (form && button) {
        form.addEventListener('submit', function () {
            button.disabled = true;
            button.textContent = 'Generating...';
        });
    }

    if (tooltipTriggers.length && window.bootstrap) {
        tooltipTriggers.map(function (trigger) {
            return new bootstrap.Tooltip(trigger);
        });
    }

    const copyButtons = document.querySelectorAll('.copy-itinerary');
    copyButtons.forEach(function (copyButton) {
        copyButton.addEventListener('click', function () {
            const target = document.querySelector(copyButton.dataset.copyTarget);
            if (!target) {
                return;
            }
            navigator.clipboard.writeText(target.textContent.trim()).then(function () {
                const originalText = copyButton.textContent;
                copyButton.textContent = 'Copied!';
                setTimeout(function () {
                    copyButton.textContent = originalText;
                }, 1500);
            });
        });
    });

    const reveals = document.querySelectorAll('.content-reveal');
    if ('IntersectionObserver' in window && reveals.length) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        reveals.forEach(function (section) {
            observer.observe(section);
        });
    } else {
        reveals.forEach(function (section) {
            section.classList.add('is-visible');
        });
    }
});
