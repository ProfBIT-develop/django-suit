(function ($) {
  $('.left-nav>ul>li:not(.active)').on('mouseenter', function() {
      var $trigger = $(this);
      var $dropdown = $trigger.find('ul');

      if ($dropdown.length === 0) return;

      $dropdown.attr('style', '');
      $trigger.css('position', 'relative');

      var dropdownHeight = $dropdown.outerHeight();
      var triggerRect = $trigger[0].getBoundingClientRect();
      var viewportHeight = $(window).height();
      var padding = 10;
      var projectedBottom = triggerRect.top + dropdownHeight;
      var bottomLimit = viewportHeight - padding;
      var newTop = 0;

      if (projectedBottom > bottomLimit) {
          var overflow = projectedBottom - bottomLimit;
          newTop = -overflow;

          if ((triggerRect.top + newTop) < padding) {
              newTop = padding - triggerRect.top;
          }

          $dropdown.css({
              'margin-top': 0,
              'top': newTop + 'px',
          });
      }
  }).on('mouseleave', function() {
      $(this).attr('style', '');
      $(this).find('ul').attr('style', '');
  });
}(Suit.$));
