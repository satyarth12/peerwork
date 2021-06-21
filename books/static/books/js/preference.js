$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-preference").modal("show");
      },
      success: function (data) {
        $("#modal-preference .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#preference-table").html(data.html_preference_list);
          $("#modal-preference").modal("hide");
        }
        else {
          $("#modal-preference .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create preference
  $(".js-create-preference").click(loadForm);
  $("#modal-preference").on("submit", ".js-preference-create-form", saveForm);

  // Update preference
  $("#preference-table").on("click", ".js-update-preference", loadForm);
  $("#modal-preference").on("submit", ".js-preference-update-form", saveForm);

$("#preference-table").on("click", ".js-delete-preference", loadForm);
$("#modal-preference").on("submit", ".js-preference-delete-form", saveForm);

});