$(document).ready(function() {
  // On the registration form only show researcher credentials if we select
  // a background that includes the word research
  if ($('#id_researcher_credentials')) {
    $('#id_researcher_credentials').parent('div').hide();
    $('#id_background').on('change', function (e) {
      var selectedText = $("option:selected", $('#id_background')).text();
      if (selectedText.indexOf("research") > -1) {
        $('#id_researcher_credentials').parent('div').show();
      } else {
        $('#id_researcher_credentials').parent('div').hide();
      }
    });
  }
});
