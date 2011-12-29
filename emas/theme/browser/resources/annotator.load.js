jQuery(function ($) {

    function maybeWaitForMathJax(fn){
        /* If mathjax is loaded, wait for it to load, otherwise go right ahead
           and call our callback */
        if(typeof MathJax === "undefined"){
            fn();
        } else {
            MathJax.Hub.Queue(fn);
        }
    }

  maybeWaitForMathJax(function () {
    if (typeof $.fn.annotator !== 'function') {
      alert("Annotator not properly installed.");
        return;
    }
    var elem = $('#content');
    if (elem.length) {
        var account_id = AnnotatorConfig.getAccountId();
        var annotator_store = AnnotatorConfig.getAnnotatorStore();
        var userid = AnnotatorConfig.getUserId();
        var absolute_url = AnnotatorConfig.getAbsoluteUrl();
        if (userid == ''){
            userid = "siyavula";
        }
        console.log(userid);

        // user name if different from userid (could be ip address if no real user)
        var options = {};
        options.permissions = {};

        // don't show the checkboxes
        options.permissions.showViewPermissionsCheckbox = false
        options.permissions.showEditPermissionsCheckbox = false
        options.permissions.user = {
            'name': userid
        };
        options.categories = {
            'errata':'annotator-hl-errata', 
            'comment':'annotator-hl-comment', 
            'suggestion':'annotator-hl-suggestion'
        };

        if(userid) {
            elem.data('annotator:headers', {'x-annotator-user-id': userid});
            // set user
            options.permissions.user.id = userid;
            // configure permissions (only owner can edit, everyone can read)
            options.permissions.permissions = {
                'read': [],
                'update': [userid],
                'delete': [userid],
                'admin': [userid]
            }
        }
        var annotator = elem.annotator().data('annotator');
        annotator.addPlugin('Store', {
            prefix: annotator_store,
            annotationData: {
                'uri': absolute_url,
                'account_id': account_id
            },
            loadFromSearch: {
                'uri': absolute_url,
                limit: -1 
            }
        });
        // when loading annotations from backend determine how to get the user id
        options.permissions.userId = function(user) {
            if (user) {
                return user.id;
            }
        };
        // ditto for human readable string for user
        options.permissions.userString = function(user) {
            if (user) {
                return user.name;
            }
        };
        annotator.addPlugin('Permissions', options.permissions);
        annotator.addPlugin('Categories', options.categories);
        annotator.addPlugin('RoundupStatus');
        annotator.addPlugin('Markdown');
    }
  });

  // The little help box on the side
  $(".annotator-help-trigger").click(function(){
      $(".annotator-help-panel").toggle("fast");
      $(this).toggleClass("active");
      return false;
  });

});
