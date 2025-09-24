document.addEventListener('DOMContentLoaded', function() {
  var body = document.body;
  var redirectUrl = body.getAttribute('data-redirect-url');
  if (redirectUrl) {
    window.location.href = redirectUrl;
  }
});