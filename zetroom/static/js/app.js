const accordionHeader = document.querySelectorAll('.questions-inner-all-accordions__accordion__header');

accordionHeader.forEach(accordionHeader => {
  accordionHeader.addEventListener('click', event => {
    const currentActiveHeader = document.querySelector('.questions-inner-all-accordions__accordion__header.active');
    if (currentActiveHeader && currentActiveHeader !== accordionHeader) {
      currentActiveHeader.classList.toggle('active');
      currentActiveHeader.nextElementSibling.style.maxHeight = 0;
    }

    accordionHeader.classList.toggle('active');
    const accordionBody = accordionHeader.nextElementSibling;

    if (accordionHeader.classList.contains('active')) {
      accordionBody.style.maxHeight = accordionBody.scrollHeight + 'px';
    } else {
      accordionBody.style.maxHeight = 0;
    }
  });
});




window.addEventListener("load", function () {
  const div = document.querySelector(".events-inner__link1");
  const window = document.querySelector(".btn-modal");
  const windowClose = document.querySelector(".close");

  div.addEventListener("click", function () {
    window.classList.toggle("active");
  });

  windowClose.addEventListener("click", function () {
    window.classList.remove("active");

  });
});

window.addEventListener("load", function () {
  const div = document.querySelector(".events-inner__link2");
  const window = document.querySelector(".btn-modal");
  const windowClose = document.querySelector(".close");

  div.addEventListener("click", function () {
    window.classList.toggle("active");
  });

  windowClose.addEventListener("click", function () {
    window.classList.remove("active");

  });
});

window.addEventListener("load", function () {
  const div = document.querySelector(".events-inner__link3");
  const window = document.querySelector(".btn-modal");
  const windowClose = document.querySelector(".close");

  div.addEventListener("click", function () {
    window.classList.toggle("active");
  });

  windowClose.addEventListener("click", function () {
    window.classList.remove("active");

  });
});

