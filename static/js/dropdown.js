// static/js/dropdown.js
document.addEventListener('DOMContentLoaded', function () {
  const dropdownToggles = document.querySelectorAll('.dropdown-submenu .dropdown-toggle');
  dropdownToggles.forEach(function (el) {
    el.addEventListener('mouseenter', function (e) {
      let submenu = el.nextElementSibling;
      if (submenu && submenu.classList.contains('dropdown-menu')) {
        submenu.classList.add('show');
      }
    });
    el.parentElement.addEventListener('mouseleave', function () {
      let submenu = el.nextElementSibling;
      if (submenu && submenu.classList.contains('dropdown-menu')) {
        submenu.classList.remove('show');
      }
    });
  });
});