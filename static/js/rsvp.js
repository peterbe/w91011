$(function() {
  $('input[name="coming"]').change(function() {
    if ($(this).val()=='yes')
      $('#form').fadeIn(600);
    else
       $('#form').fadeOut(600);
  });
  if ($('input[name="coming"]:checked').val()=='yes')
    $('#form').show();

  if ($('input[name="coming"]:checked').size()) {
    if ($('input[name="coming"]:checked').val()=='yes')
      $('#form').fadeIn(100);
    else
       $('#form').fadeOut(100);
  }
});
