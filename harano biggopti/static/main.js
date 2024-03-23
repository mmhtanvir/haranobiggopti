function showPopup(popupId) {
    var popup = document.getElementById(popupId);
    if (popup) {
      popup.classList.remove('hidden');
    }
  }

  function hidePopup() {
    var popups = document.querySelectorAll('.common');
    popups.forEach(function(popup) {
      popup.classList.add('hidden');
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.showPopupButton');
    buttons.forEach(function(button) {
      button.addEventListener('click', function() {
        var popupId = this.getAttribute('data-popup-id');
        showPopup(popupId);
      });
    });
  });
