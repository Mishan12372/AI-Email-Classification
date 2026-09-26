/* =========================================================
EMAIL AI - PROFESSIONAL JAVASCRIPT
AI Email Classification and Reply Suggestion System
========================================================= */

document.addEventListener("DOMContentLoaded", function () {


console.log("✓ EmailAI system loaded successfully.");


/* =====================================================
   ACTIVE NAVIGATION
===================================================== */

const currentPage = window.location.pathname;

const navLinks = document.querySelectorAll(".nav-links a");

navLinks.forEach(function (link) {

    const linkPath = new URL(
        link.href,
        window.location.origin
    ).pathname;

    link.classList.remove("active");

    if (
        linkPath === currentPage ||
        (currentPage === "/" && linkPath === "/")
    ) {
        link.classList.add("active");
    }

});


/* =====================================================
   EMAIL FORM
===================================================== */

const emailForm = document.querySelector("form");

const subjectInput =
    document.getElementById("subject");

const bodyInput =
    document.getElementById("body");


if (emailForm && subjectInput && bodyInput) {


    /* ================================================
       INPUT FOCUS EFFECT
    ================================================= */

    const inputs = [
        subjectInput,
        bodyInput
    ];

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            input.classList.add("input-focused");

        });


        input.addEventListener("blur", function () {

            input.classList.remove("input-focused");

        });

    });


    /* ================================================
       FORM VALIDATION
    ================================================= */

    emailForm.addEventListener(
        "submit",
        function (event) {

            const subject =
                subjectInput.value.trim();

            const body =
                bodyInput.value.trim();


            /* Empty email */

            if (
                subject === "" &&
                body === ""
            ) {

                event.preventDefault();

                showMessage(
                    "Please enter an email subject or email body.",
                    "error"
                );

                subjectInput.focus();

                return;

            }


            /* Very short input */

            if (
                subject.length < 2 &&
                body.length < 5
            ) {

                event.preventDefault();

                showMessage(
                    "Please enter a little more email content.",
                    "warning"
                );

                return;

            }


            /* ========================================
               LOADING STATE
            ======================================== */

            const submitButton =
                emailForm.querySelector(
                    "button[type='submit']"
                );


            if (submitButton) {

                submitButton.disabled = true;

                submitButton.classList.add(
                    "loading"
                );

                submitButton.innerHTML =
                    '<span class="loading-spinner"></span> Analyzing Email...';

            }


            console.log(
                "Email submitted for analysis."
            );

        }
    );


    /* ================================================
       CHARACTER COUNTERS
    ================================================= */

    createCounter(
        subjectInput,
        150,
        "subject-counter"
    );

    createCounter(
        bodyInput,
        3000,
        "body-counter"
    );

}


/* =====================================================
   AUTO HIDE ALERTS
===================================================== */

const alerts =
    document.querySelectorAll(".alert");


alerts.forEach(function (alert) {

    setTimeout(function () {

        alert.style.opacity = "0";

        alert.style.transform =
            "translateY(-8px)";

        setTimeout(function () {

            alert.remove();

        }, 400);

    }, 4000);

});



/* =====================================================
   HISTORY PAGE
===================================================== */

const historyRows =
    document.querySelectorAll(
        "table tbody tr"
    );


if (historyRows.length > 0) {

    console.log(
        historyRows.length +
        " prediction(s) found in history."
    );


    /* Add subtle row interaction */

    historyRows.forEach(function (row) {

        row.addEventListener(
            "mouseenter",
            function () {

                row.classList.add(
                    "history-row-hover"
                );

            }
        );


        row.addEventListener(
            "mouseleave",
            function () {

                row.classList.remove(
                    "history-row-hover"
                );

            }
        );

    });

}



/* =====================================================
   COPY SUGGESTED REPLY
===================================================== */

const replyText =
    document.querySelector(
        ".reply-content p"
    );


if (replyText) {

    const replyBox =
        document.querySelector(
            ".reply-content"
        );


    if (replyBox) {

        const copyButton =
            document.createElement("button");

        copyButton.type = "button";

        copyButton.className =
            "copy-reply-btn";

        copyButton.innerHTML =
            "📋 Copy Reply";


        replyBox.appendChild(
            copyButton
        );


        copyButton.addEventListener(
            "click",
            function () {

                const text =
                    replyText.innerText.trim();


                if (!text) {

                    showMessage(
                        "No reply available to copy.",
                        "error"
                    );

                    return;

                }


                navigator.clipboard.writeText(text)
                    .then(function () {

                        copyButton.innerHTML =
                            "✓ Copied!";

                        copyButton.classList.add(
                            "copied"
                        );


                        showMessage(
                            "Suggested reply copied successfully.",
                            "success"
                        );


                        setTimeout(function () {

                            copyButton.innerHTML =
                                "📋 Copy Reply";

                            copyButton.classList.remove(
                                "copied"
                            );

                        }, 2000);

                    })
                    .catch(function () {

                        showMessage(
                            "Unable to copy the reply.",
                            "error"
                        );

                    });

            }
        );

    }

}



/* =====================================================
   SMOOTH SCROLL
===================================================== */

const internalLinks =
    document.querySelectorAll(
        'a[href^="#"]'
    );


internalLinks.forEach(function (link) {

    link.addEventListener(
        "click",
        function (event) {

            const targetId =
                link.getAttribute("href");


            if (
                targetId &&
                targetId !== "#"
            ) {

                const target =
                    document.querySelector(
                        targetId
                    );


                if (target) {

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }

            }

        }
    );

});



/* =====================================================
   SCROLL REVEAL
===================================================== */

const revealElements =
    document.querySelectorAll(
        ".feature-card, " +
        ".home-feature-card, " +
        ".process-step, " +
        ".prediction-card, " +
        ".result-email-card, " +
        ".reply-result-card, " +
        ".about-card, " +
        ".history-card"
    );


if (
    "IntersectionObserver" in window &&
    revealElements.length > 0
) {

    const observer =
        new IntersectionObserver(
            function (entries) {

                entries.forEach(
                    function (entry) {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "visible"
                            );

                            observer.unobserve(
                                entry.target
                            );

                        }

                    }
                );

            },
            {
                threshold: 0.12
            }
        );


    revealElements.forEach(
        function (element) {

            element.classList.add(
                "reveal"
            );

            observer.observe(
                element
            );

        }
    );

}



/* =====================================================
   PAGE LOAD
===================================================== */

document.body.classList.add(
    "page-loaded"
);


console.log(
    "✓ Machine Learning Email Classification Interface Ready."
);


});

/* =========================================================
SHOW MESSAGE
========================================================= */

function showMessage(message, type) {


/* Remove previous message */

const oldMessage =
    document.querySelector(
        ".custom-message"
    );


if (oldMessage) {

    oldMessage.remove();

}


const messageBox =
    document.createElement("div");


messageBox.className =
    "custom-message " +
    "message-" +
    type;


let icon = "ℹ️";


if (type === "error") {

    icon = "❌";

}
else if (type === "warning") {

    icon = "⚠️";

}
else if (type === "success") {

    icon = "✓";

}


messageBox.innerHTML =
    "<span>" +
    icon +
    "</span>" +
    "<p>" +
    message +
    "</p>";


document.body.appendChild(
    messageBox
);


setTimeout(function () {

    messageBox.classList.add(
        "message-hide"
    );


    setTimeout(function () {

        messageBox.remove();

    }, 350);

}, 3500);


}

/* =========================================================
CHARACTER COUNTER
========================================================= */

function createCounter(
input,
maxLength,
className
) {


if (!input) {

    return;

}


const counter =
    document.createElement("div");


counter.className =
    className;


counter.style.textAlign =
    "right";

counter.style.fontSize =
    "10px";

counter.style.color =
    "#929aaa";

counter.style.marginTop =
    "5px";


input.parentNode.insertBefore(
    counter,
    input.nextSibling
);


function updateCounter() {

    const currentLength =
        input.value.length;


    counter.textContent =
        currentLength +
        " / " +
        maxLength;


    if (
        currentLength >
        maxLength * 0.9
    ) {

        counter.style.color =
            "#ef4444";

    }
    else {

        counter.style.color =
            "#929aaa";

    }

}


input.addEventListener(
    "input",
    updateCounter
);


updateCounter();


}
