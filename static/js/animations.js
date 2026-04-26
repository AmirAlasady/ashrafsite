(function () {
    function initRevealAnimations() {
        var items = document.querySelectorAll(".animate");
        if (!items.length) return;

        if (!("IntersectionObserver" in window)) {
            items.forEach(function (el) { el.classList.add("in-view"); });
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

        items.forEach(function (el) { observer.observe(el); });
    }

    function initBtsSlider() {
        var slider = document.querySelector(".bts-slider");
        if (!slider) return;

        var track = slider.querySelector(".bts-track");
        var slides = track.querySelectorAll(".bts-slide");
        var prev = slider.querySelector(".bts-btn-prev");
        var next = slider.querySelector(".bts-btn-next");
        if (!slides.length || !prev || !next) return;

        var idx = 0;
        var total = slides.length;

        function gapPx() {
            var gap = parseFloat(getComputedStyle(track).gap || "16");
            return isNaN(gap) ? 16 : gap;
        }

        function slidePx() {
            return slides[0].offsetWidth + gapPx();
        }

        function goTo(newIdx) {
            idx = ((newIdx % total) + total) % total;
            track.style.transform = "translateX(" + (-idx * slidePx()) + "px)";
        }

        prev.addEventListener("click", function () { goTo(idx - 1); });
        next.addEventListener("click", function () { goTo(idx + 1); });

        var resizeTimer;
        window.addEventListener("resize", function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () { goTo(idx); }, 80);
        });

        // Keyboard support when slider is focused
        slider.tabIndex = 0;
        slider.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft") { goTo(idx - 1); }
            if (e.key === "ArrowRight") { goTo(idx + 1); }
        });

        goTo(0);
    }

    function init() {
        initRevealAnimations();
        initBtsSlider();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
