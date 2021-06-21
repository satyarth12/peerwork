$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-profile").modal("show");
      },
      success: function (data) {
        $("#modal-profile .modal-content").html(data.html_form);
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
          $("#profile-table").html(data.html_profile_list);
          $("#modal-profile").modal("hide");
        }
        else {
          $("#modal-profile .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create profile
  $(".js-create-profile").click(loadForm);
  $("#modal-profile").on("submit", ".js-profile-create-form", saveForm);

  // Update profile
  $("#profile-table").on("click", ".js-update-profile", loadForm);
  $("#modal-profile").on("submit", ".js-profile-update-form", saveForm);

$("#profile-table").on("click", ".js-delete-profile", loadForm);
$("#modal-profile").on("submit", ".js-profile-delete-form", saveForm);

});