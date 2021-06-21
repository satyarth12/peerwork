$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-link").modal("show");
      },
      success: function (data) {
        $("#modal-link .modal-content").html(data.html_form);
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
          $("#link-table").html(data.html_link_list);
          $("#modal-link").modal("hide");
        }
        else {
          $("#modal-link .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create link
  $(".js-create-link").click(loadForm);
  $("#modal-link").on("submit", ".js-link-create-form", saveForm);

  // Update link
  $("#link-table").on("click", ".js-update-link", loadForm);
  $("#modal-link").on("submit", ".js-link-update-form", saveForm);

$("#link-table").on("click", ".js-delete-link", loadForm);
$("#modal-link").on("submit", ".js-link-delete-form", saveForm);

});