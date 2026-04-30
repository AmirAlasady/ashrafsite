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

        var viewport = slider.querySelector(".bts-viewport");
        var track = slider.querySelector(".bts-track");
        var slides = track.querySelectorAll(".bts-slide");
        var prev = slider.querySelector(".bts-btn-prev");
        var next = slider.querySelector(".bts-btn-next");
        if (!slides.length || !prev || !next || !viewport) return;

        var idx = 0;
        var total = slides.length;
        var AUTO_INTERVAL_MS = 3500;
        var autoTimer = null;
        var prefersReducedMotion = window.matchMedia &&
            window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        function gapPx() {
            var gap = parseFloat(getComputedStyle(track).gap || "16");
            return isNaN(gap) ? 16 : gap;
        }

        function goTo(newIdx) {
            idx = ((newIdx % total) + total) % total;
            var slideWidth = slides[0].offsetWidth;
            var stride = slideWidth + gapPx();
            // Center the active slide inside the viewport
            var sidePeek = (viewport.offsetWidth - slideWidth) / 2;
            var translate = sidePeek - idx * stride;
            track.style.transform = "translateX(" + translate + "px)";

            slides.forEach(function (s, i) {
                s.classList.toggle("is-active", i === idx);
            });
        }

        function startAuto() {
            if (autoTimer || prefersReducedMotion || total < 2) return;
            autoTimer = setInterval(function () { goTo(idx + 1); }, AUTO_INTERVAL_MS);
        }
        function stopAuto() {
            if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
        }
        function restartAuto() { stopAuto(); startAuto(); }

        prev.addEventListener("click", function () { goTo(idx - 1); restartAuto(); });
        next.addEventListener("click", function () { goTo(idx + 1); restartAuto(); });

        // Click a peek slide to focus it
        slides.forEach(function (s, i) {
            s.addEventListener("click", function () {
                if (i !== idx) { goTo(i); restartAuto(); }
            });
        });

        // Pause on hover/focus, resume on leave
        slider.addEventListener("mouseenter", stopAuto);
        slider.addEventListener("mouseleave", startAuto);
        slider.addEventListener("focusin", stopAuto);
        slider.addEventListener("focusout", startAuto);
        // Pause when the tab isn't visible (saves battery, prevents drift)
        document.addEventListener("visibilitychange", function () {
            if (document.hidden) stopAuto(); else startAuto();
        });

        var resizeTimer;
        window.addEventListener("resize", function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () { goTo(idx); }, 80);
        });

        // Keyboard support when slider is focused
        slider.tabIndex = 0;
        slider.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft")  { goTo(idx - 1); restartAuto(); }
            if (e.key === "ArrowRight") { goTo(idx + 1); restartAuto(); }
        });

        goTo(0);
        startAuto();
    }

    function initClientsMarquee() {
        var marquee = document.querySelector(".clients-marquee");
        if (!marquee) return;
        var track = marquee.querySelector(".clients-track");
        if (!track) return;

        var originalItems = Array.prototype.slice.call(track.children);
        if (!originalItems.length) return;

        function setSetWidthAndClone() {
            // Reset to the original set only
            while (track.children.length > originalItems.length) {
                track.removeChild(track.lastChild);
            }

            var setWidth = 0;
            originalItems.forEach(function (el) { setWidth += el.offsetWidth; });
            if (setWidth <= 0) return;

            // Clone until total track width >= 3x viewport. That guarantees
            // the visible portion always shows >= 2 viewports worth of items,
            // so when the loop resets the right edge is never empty.
            var minWidth = Math.max(window.innerWidth * 3, setWidth * 2);
            var totalWidth = setWidth;
            while (totalWidth < minWidth) {
                originalItems.forEach(function (el) {
                    var clone = el.cloneNode(true);
                    clone.setAttribute("aria-hidden", "true");
                    var link = clone.querySelector("a");
                    if (link) link.setAttribute("tabindex", "-1");
                    track.appendChild(clone);
                });
                totalWidth += setWidth;
            }

            track.style.setProperty("--marquee-set-width", setWidth + "px");
            track.classList.add("is-ready");
        }

        // Wait for images so offsetWidth is accurate
        var imgs = track.querySelectorAll("img");
        var pending = imgs.length;
        if (pending === 0) {
            setSetWidthAndClone();
        } else {
            imgs.forEach(function (img) {
                if (img.complete) {
                    if (--pending === 0) setSetWidthAndClone();
                } else {
                    img.addEventListener("load", function () {
                        if (--pending === 0) setSetWidthAndClone();
                    });
                    img.addEventListener("error", function () {
                        if (--pending === 0) setSetWidthAndClone();
                    });
                }
            });
            // Fallback in case events never fire
            setTimeout(setSetWidthAndClone, 1500);
        }

        var resizeTimer;
        window.addEventListener("resize", function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(setSetWidthAndClone, 200);
        });
    }

    function init() {
        initRevealAnimations();
        initBtsSlider();
        initClientsMarquee();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
