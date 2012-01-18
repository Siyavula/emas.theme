(function() {
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  };
  Annotator.Plugin.RoundupStatus = (function() {
    __extends(RoundupStatus, Annotator.Plugin);
    RoundupStatus.prototype.options = {
      status: {}
    };
    function RoundupStatus(element, status) {
      this.options.status = status;
    }
    RoundupStatus.prototype.pluginInit = function() {
      if (!Annotator.supported()) {
        return;
      }
      this.viewer = this.annotator.viewer.addField({
        load: this.updateViewer
      });
      if (this.annotator.plugins.Filter) {
        return this.annotator.plugins.Filter.addFilter({
          label: 'Status',
          property: 'status',
          isFiltered: Annotator.Plugin.RoundupStatus.filterCallback
        });
      }
    };
    RoundupStatus.prototype.updateViewer = function(field, annotation) {
      field = $(field);
      if (annotation.issue_id != null) {
        return field.addClass('annotator-status').html(function() {
          var string;
          return string = '<a href="http://roundup.emas.upfronthosting.co.za/emas/issue' + annotation.issue_id + '" target="_blank">See comments on Roundup!</a>';
        });
      } else {
        return field.remove();
      }
    };
    return RoundupStatus;
  })();
}).call(this);
