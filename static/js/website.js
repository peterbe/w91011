function L() {
   if (window.console && window.console.log)
     console.log.apply(console, arguments);
}


$(function() {
   if ($('#id_username_or_email').size()) {
      $.each({'#id_username_or_email':'your email address',
         '#id_password': 'sample'
      }, function(key, value) {
         if (!$(key).val()) {
            $(key)
              .val(value)
                .addClass('placeholder')
                  .bind('focus', function() {
                     if ($(this).val() == value) {
                        $(this).val('').removeClass('placeholder');
                     }
                  })
                    .bind('blur', function() {
                       if (!$(this).val()) {
                          $(this).val(value).addClass('placeholder');
                       }
                    });
         }
      });

   }
});