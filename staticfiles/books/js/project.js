$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-project").modal("show");
      },
      success: function (data) {
        $("#modal-project .modal-content").html(data.html_form);
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
          $("#project-table").html(data.html_project_list);
          $("#modal-project").modal("hide");
        }
        else {
          $("#modal-project .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create project
  $(".js-create-project").click(loadForm);
  $("#modal-project").on("submit", ".js-project-create-form", saveForm);

  // Update project
  $("#project-table").on("click", ".js-update-project", loadForm);
  $("#modal-project").on("submit", ".js-project-update-form", saveForm);

$("#project-table").on("click", ".js-delete-project", loadForm);
$("#modal-project").on("submit", ".js-project-delete-form", saveForm);

});