var cbgen = function (selector) {
  return function (color) {
    var xs = $(selector);
    xs.get(0).value = color;
    if (xs.get(0).value) {
      this.setColor(xs.get(0).value);
      xs.get(0).style.background = color;
    }

    if ($(selector + '-updateval').get(0).checked) {
        /* We are now using AJAX mofo! */
        var form = xs.parents('form:first');
        var formobj = form.get(0);
        if (formobj[selector] && formobj[selector] == color) {
            return;
        }
        formobj[selector] = color;
        var data = {};
        var results = form.find("input,select,textarea");
        for (var i in results) {
            var elem = results[i];
            if (elem.type != "checkbox" || elem.checked) {
                data[elem.name] = elem.value;
            }
        }
        $.post(location.href, data);
    }
  };
};
