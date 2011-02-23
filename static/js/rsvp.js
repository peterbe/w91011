$(function() {
  $('input[name="coming"]').change(function() {
    if ($(this).val()=='yes')
      $('#form').fadeIn(600);
  });
  if ($('input[name="coming"]:checked').val()=='yes')
    $('#form').show();
});
