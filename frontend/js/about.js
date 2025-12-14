document.addEventListener('DOMContentLoaded', function () {

    const lenis = new Lenis({
        autoRaf: true,
        wheelMultiplier: 0.7,
        touchMultiplier: 0.8,
    });

    const swiper = new Swiper('.swiper', {
        direction: 'horizontal',
        loop: true,

        navigation: {
            nextEl: '.swiper_button_next',
            prevEl: '.swiper_button_prev',
        },
    });


    
});