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
    var elem = $('#content');
    if (elem.length) {
        var account_id = '0b776919ee56436a11fdd72b3f001a23';
        var annotator_store = 'http://192.168.0.7:5000/api';
        var userid = null;
        while (userid == null){
            userid = prompt("Please enter your dummy user name, for testing","");
            console.log(userid);
        }
        if (userid == ''){
            userid = "siyavula";
        }
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
                'uri':  'http://192.168.0.7/cnxdemo/pr01.html',
                // set account id
                'account_id': account_id
            },
            loadFromSearch: {
                'uri': 'http://192.168.0.7/cnxdemo/pr01.html',
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
});
