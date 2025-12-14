document.addEventListener('DOMContentLoaded', function () {

    const lenis = new Lenis({
        autoRaf: true,
        wheelMultiplier: 0.7,
        touchMultiplier: 0.8,
    });




    const imgDefault = document.getElementById("default");
    const imgEvent = document.getElementById("event");
    const imgDestination = document.getElementById("destination");
    const imgExcursion = document.getElementById("excursion");

    const cardDefault = document.getElementById("defaultCard");
    const cardEvent = document.getElementById("eventCard");
    const cardDestination = document.getElementById("destinationCard");
    const cardExcursion = document.getElementById("excursionCard");

    const images = [imgDefault, imgEvent, imgDestination, imgExcursion];

    const cardImagePairs = [
        { card: cardDefault, img: imgDefault },
        { card: cardEvent, img: imgEvent },
        { card: cardDestination, img: imgDestination },
        { card: cardExcursion, img: imgExcursion }
    ];

    function setActive(activeImg) {
        images.forEach(img => img.classList.remove("active"));
        activeImg.classList.add("active");
    }

    function removeActive() {
        images.forEach(img => img.classList.remove("active"));
    }

    cardImagePairs.forEach(pair => {
        if (pair.card && pair.img) {
            pair.card.addEventListener("pointerenter", () => setActive(pair.img));
        }
    });


    const swiper = new Swiper('.swiper', {
        direction: 'horizontal',
        loop: true,

        navigation: {
            nextEl: '.swiper_button_next',
            prevEl: '.swiper_button_prev',
        },
    });

    const faqCard = document.querySelectorAll(".questionCard");

    faqCard.forEach((card) => {
        card.addEventListener("click", function () {
            faqCard.forEach((c) => c.classList.remove("active"));
            card.classList.add("active");
        });
    });





    const hotelCard = document.querySelectorAll(".hotelCard")
    hotelCard.forEach(card => {
        card.addEventListener("click", function () {
            window.location.href = './pages/discover.html'
        })
    });

    const profile = document.querySelector("#profile")
    const logIn = document.querySelector("#logIn")
    const terms = document.querySelector("#terms")
    const submitBtn = document.querySelector("#submitBtn")


    const authenticate = () => {
        if (terms.checked) {
            submitBtn.addEventListener("click", function () {
                logIn.style.display = "none"
                profile.style.display = "block"
                window.location.href = "profile.html"
            })
        }
        else {
            console.log("You left the checkbox unchecked!")
            logIn.style.display = "block"
            profile.style.display = "none"
        }
    }
    authenticate()

});