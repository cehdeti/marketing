(function($) {
  $(document).ready(function() {
    var $carousel = $('#preview');

    if ($carousel.length > 0) {
      $carousel.carousel({
        interval: false,
      });

      $(document).bind('keyup', function(event) {
        switch (event.keyCode) {
          case 37:
            $carousel.carousel('prev');
            break;
          case 39:
            $carousel.carousel('next');
            break;
        }
      });
    }

    if ($.isFunction($.fn.popover)) {
      $('#preview .slide-waypoint').popover();
    }
  });
})(jQuery);
