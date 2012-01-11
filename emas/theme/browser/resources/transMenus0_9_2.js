//////////////////////////////////////////////////////////////////////
//* TransMenus version 0.9.2 by A. Heinrich http://www.archomai.org *//
//////////////////////////////////////////////////////////////////////
//Namespacing//
if (!org) {
    var org = {};
}
if (!org.archomai) {
    org.archomai = {};
}
if (!org.archomai.transMenus) {
    org.archomai.transMenus = {};
}
if (!org.archomai.transMenus.Persist) {
    org.archomai.transMenus.Persist = {};
}
//////////////////////////////////////////////////////
/////COLLAPSIBLE MENU BULLET IMAGE SOURCES////////////
/////SET TO "NULL" IF NONE ARE SPECIFIED//////////////
//////////////////////////////////////////////////////
org.archomai.transMenus.collapsibleMenuImages =
{
openImage : "http://m.cnx.org/transmenus/minus.gif" ,
            closedImage : "http://m.cnx.org/transmenus/plus.gif",
            height : "9px",
            width : "9px",
            space : "0px",
            moveLeft : "13px"
}
//////////////////////////////////////////////////////
///POPUP MENU SUBMENU OFFSETS IN PIXELS- PUBLIC///////
///NUMBER OF PIXELS SUBMENUS WILL BE OFFSET FROM//////
///THEIR DEFAULT POSITION/////////////////////////////
//////////////////////////////////////////////////////
org.archomai.transMenus.relativeOffsetLeft = -4;
org.archomai.transMenus.relativeOffsetTop = 0;
//////////////////////////////////////////////////////
/////COOKIE NAME //////////////
/////SET TO null TO DISABLE PERSISTENCE///////////////
//////////////////////////////////////////////////////
org.archomai.transMenus.Persist.cookiename = "__tm_state"
org.archomai.transMenus.Persist.defaultExpanded = true
///////////////////////////////////////////////
///////////////////////////////////////////////
org.archomai.transMenus.findChildNode = function(node, eltName)
{
    var retnode;
    var child;
    var children = node.childNodes;
    for (var x = 0; x < children.length && !retnode; x++) {
        child = children[x];
        if (child && child.nodeName.toLowerCase()==eltName.toLowerCase()) {
            retnode = child;
        }
    }
    return retnode;
}
org.archomai.transMenus.standards = (document.getElementById && document.getElementsByTagName);
org.archomai.transMenus.MenuRegistry = {} ;
org.archomai.transMenus.Menu = function(id)
{
    this.id = id;
    this.menuElement = document.getElementById(id);
    this.timerId = null;
    this.isOpen = false;
    this.inLimbo = false;
    this.ancestorMenuIds = new Array();
    this.childrenMenuIds = new Array();
    this.gRef = this.id + "_Menu";
    eval(this.gRef + "=this");
    this.baseUL = null;
    org.archomai.transMenus.MenuRegistry[this.id] = this;
    this.Hide = function() {
        if (this.timerId) this.timerId = window.clearTimeout(this.timerId);
        if (this.isOpen) {
            this.menuElement.style.display = "none";
            this.menuElement.style.visibility = "hidden";
            this.isOpen = false;
        }
    }
    this.ScheduleHide = function() {
        if (this.timerId) this.timerId = window.clearTimeout(this.timerId);
        this.timerId = window.setTimeout(this.gRef + ".Hide()",500);
    }
    this.HandleMouseOver = function() {
        if (this.inLimbo) {
            this.menuElement.onmouseout = new Function("eval('org.archomai.transMenus.MenuRegistry[\"' + this.id + '\"].ScheduleHide()')");
            this.inLimbo = false;
        }
        if (this.timerId) {
            this.timerId = window.clearTimeout(this.timerId);
        }
        if (!this.isOpen) {
            for (var i in org.archomai.transMenus.MenuRegistry) {
                var qualified = true;
                if (org.archomai.transMenus.MenuRegistry[i].id == this.id) qualified = false
                else if (this.ancestorMenuIds.length>0) {
                    for (var j = 0; j < this.ancestorMenuIds.length; j++) {
                        if (org.archomai.transMenus.MenuRegistry[i].id == this.ancestorMenuIds[j]) qualified = false;
                    }
                }
                if (qualified) org.archomai.transMenus.MenuRegistry[i].Hide();
            }
            this.isOpen = true;
            this.inLimbo = true;
            this.setMenuDisplay();
            this.menuElement.onmouseover = new Function("eval('org.archomai.transMenus.MenuRegistry[\"' + this.id + '\"].HandleMouseOver()')");
        }
    }
    this.HandleMouseDown = function() {
        var inarray = false;
        var nowclass = "";
        var node;
        for (var x = 0; !inarray && x < org.archomai.transMenus.highlight.length; x++) {
            if (org.archomai.transMenus.highlight[x] == this.menuElement.id) inarray = true;
        }
        if (this.menuElement.style.display == "none") {
            this.menuElement.style.display = "block";
            if (org.archomai.transMenus.collapsibleMenuImages.openImage) {
                this.menuElement.parentNode.firstChild.setAttribute('src',
                        org.archomai.transMenus.collapsibleMenuImages.openImage);
            }
            if (inarray) {
                node = org.archomai.transMenus.findChildNode(this.menuElement.parentNode, 'H4')
                    if (node.oldclass) {
                        node.className = node.oldclass;
                    } else {
                        node.className = "";
                    }
            }
        } else {
            this.menuElement.style.display = "none";
            if (org.archomai.transMenus.collapsibleMenuImages.closedImage) {
                this.menuElement.parentNode.firstChild.setAttribute('src',
                        org.archomai.transMenus.collapsibleMenuImages.closedImage);
            }
            if (inarray) {
                node = org.archomai.transMenus.findChildNode(this.menuElement.parentNode, 'H4')
                    nowclass = node.className;
                node.oldclass = nowclass;
                node.className = "cnx_current " + nowclass;
            }
        }
        if (this.menuElement.gentle) {
            this.menuElement.gentle = false; // ToC special: if we change state, wipe special treatment
        }
        org.archomai.transMenus.Persist.setState();
    }
    this.setMenuDisplay = function() {
        var trigger = this.menuElement.parentNode;
        var x, y;
        if (trigger.parentNode.className == "popUpMenu") {
            x = trigger.offsetLeft + trigger.parentNode.offsetWidth + org.archomai.transMenus.relativeOffsetLeft;
            y = trigger.offsetTop + org.archomai.transMenus.relativeOffsetTop;
        } else {
            var masterOffsetX = 0;
            var masterOffsetY = 0;
            var tempEl = trigger;
            while (tempEl.offsetParent != null) {
                masterOffsetX += tempEl.offsetLeft;
                masterOffsetY += tempEl.offsetTop;
                tempEl = tempEl.offsetParent;
            }
            x = (document.all) ? (document.body.offsetLeft + masterOffsetX) : masterOffsetX;
            y = (document.all) ? (document.body.offsetTop + masterOffsetY) : masterOffsetY;
            y += trigger.parentNode.offsetHeight;
        }
        this.menuElement.style.left = x + "px";
        this.menuElement.style.top = y + "px";
        this.menuElement.style.display = "block";
        this.menuElement.style.visibility = "visible";
    }
} ;
org.archomai.transMenus.ShowMenu = function(e)
{
    var eventTarget = (document.all) ? event.srcElement : e.target;
    eventTarget = (eventTarget.subMenu) ? eventTarget : eventTarget.parentNode;
    if (eventTarget.subMenu) org.archomai.transMenus.MenuRegistry[eventTarget.subMenu].HandleMouseOver();
} ;
org.archomai.transMenus.HideMenu = function(e)
{
    var eventTarget = (document.all) ? event.srcElement : e.target;
    eventTarget = (eventTarget.subMenu) ? eventTarget : eventTarget.parentNode;
    if (eventTarget.subMenu) org.archomai.transMenus.MenuRegistry[eventTarget.subMenu].ScheduleHide();
} ;
org.archomai.transMenus.ExpandMenu = function(e)
{
    var eventTarget = (document.all) ? event.srcElement : e.target;
    if (eventTarget.subMenu) {
        org.archomai.transMenus.MenuRegistry[eventTarget.subMenu].HandleMouseDown();
        if (document.all) event.cancelBubble = true;
        if (e && !document.all) e.stopPropagation();
    }
} ;
org.archomai.transMenus.Persist.state = {};
org.archomai.transMenus.Persist.setState = function()
{
    if (org.archomai.transMenus.Persist.cookiename != null) {
        var ListArray = document.getElementsByTagName("ul");
        var expanded = [];
        var x = 0;
        for (var i=0;i<ListArray.length;i++) {
            if ((ListArray[i].className == 'collapsibleMenu') &&
                    (!ListArray[i].gentle) && // ToC special: don't persist auto-expanded nodes
                    ((org.archomai.transMenus.Persist.defaultExpanded && ListArray[i].style.display=="none") ||
                     (!org.archomai.transMenus.Persist.defaultExpanded && ListArray[i].style.display!="none"))) {
                expanded[x] = ListArray[i].id;
                x++;
            }
        }
        expanded = escape(expanded.join())
            var expires = new Date();
        expires.setFullYear(expires.getFullYear() + 1); // one year from now
        var course = document.getElementById("course");
        var path = "/";
        if (course) {
            path = course.getAttribute("path");
        }
        document.cookie = org.archomai.transMenus.Persist.cookiename + "=" + expanded
            + "; expires=" + expires.toGMTString()
            + "; path=" + path;
    }
};
org.archomai.transMenus.Persist.getState = function()
{
    if (org.archomai.transMenus.Persist.cookiename != null) {
        var allcookies = document.cookie;
        var pos = allcookies.indexOf(org.archomai.transMenus.Persist.cookiename + "=");
        if (pos != -1) {
            var start = pos + org.archomai.transMenus.Persist.cookiename.length + 1;
            var end = allcookies.indexOf(";", start);
            if (end == -1) end = allcookies.length;
            var value = allcookies.substring(start, end);
            value = unescape(value);
            value = value.split(",");
            var elt;
            org.archomai.transMenus.Persist.state = {};
            for (var x=0; x < value.length; x++) {
                org.archomai.transMenus.Persist.state[value[x]] = true
            }
        } else {
            org.archomai.transMenus.Persist.state = {};
        }
    }
};
org.archomai.transMenus.Persist.isExpanded = function(id)
{
    var expanded = org.archomai.transMenus.Persist.defaultExpanded;
    if (org.archomai.transMenus.Persist.state[id] == true) {
        expanded = !expanded;
    }
    return expanded;
};
org.archomai.transMenus.highlight = new Array();
org.archomai.transMenus.setupMovingHighlight = function()
{
    // this will only work with one tree. multiple is possible, but WAGNI.
    var current = document.getElementById("current")
        if (current) {
            current = current.parentNode;
            var x = 0;
            while (current != null && current.id != "collapsibleDemo") {
                if (current.id != "" && current.id != null) {
                    org.archomai.transMenus.highlight[x] = current.id;
                    x++;
                }
                current = current.parentNode;
            }
        }
};
org.archomai.transMenus.initHighlight = function()
{
    for (var x = 0; x < org.archomai.transMenus.highlight.length; x++) {
        var elt = document.getElementById(org.archomai.transMenus.highlight[x]);
        if (elt.style.display == "none") {
            elt.parentNode.childNodes[2].className = "cnx_current";
        }
    }
}
org.archomai.transMenus.MenuSetup = function()
{
    org.archomai.transMenus.Persist.getState();
    //org.archomai.transMenus.SetStylesheet();
    var ListArray = document.getElementsByTagName("ul");
    var j = 0;
    for (var i=0;i<ListArray.length;i++) {
        if (ListArray[i].className == "popUpMenu") {
            if (!ListArray[i].id) {ListArray[i].id = "Menu_" + j; j++ }
            ListArray[i].style.position = "absolute";
            ListArray[i].style.display = "none";
            new org.archomai.transMenus.Menu(ListArray[i].id);
            if (ListArray[i].parentNode.parentNode.className == "popUpMenu") {
                org.archomai.transMenus.MenuRegistry[ListArray[i].id].ancestorMenuIds[0] = ListArray[i].parentNode.parentNode.id;
                org.archomai.transMenus.MenuRegistry[ListArray[i].id].ancestorMenuIds = org.archomai.transMenus.MenuRegistry[ListArray[i].id].ancestorMenuIds.concat(org.archomai.transMenus.MenuRegistry[ListArray[i].parentNode.parentNode.id].ancestorMenuIds)
            }
            if (ListArray[i].parentNode.parentNode.className != "popUpMenu") org.archomai.transMenus.MenuRegistry[ListArray[i].id].baseUL = ListArray[i].parentNode.parentNode;
            var triggerElement = (ListArray[i].parentNode.firstChild.nodeType == 3) ? ListArray[i].parentNode : ListArray[i].parentNode.firstChild;
            if (triggerElement.style.cursor) triggerElement.style.cursor = "pointer";
            triggerElement.subMenu = ListArray[i].id;
            if (triggerElement.addEventListener) {
                triggerElement.addEventListener("mouseover",org.archomai.transMenus.ShowMenu,false);
                triggerElement.addEventListener("mouseout",org.archomai.transMenus.HideMenu,false);
            } else if (triggerElement.attachEvent) {
                triggerElement.attachEvent("onmouseover",org.archomai.transMenus.ShowMenu);
                triggerElement.attachEvent("onmouseout",org.archomai.transMenus.HideMenu);
            }
        } else if (ListArray[i].className == "collapsibleMenu") {
            if (!ListArray[i].id) {ListArray[i].id = "Menu_" + j; j++ }
            new org.archomai.transMenus.Menu(ListArray[i].id);
            if (!org.archomai.transMenus.Persist.isExpanded(ListArray[i].id)) {
                ListArray[i].style.display = "none";
            }
            var triggerElement = ListArray[i].parentNode;
            var twistyImage = document.createElement('img');
            twistyImage.style.height = org.archomai.transMenus.collapsibleMenuImages.height
                twistyImage.style.width = org.archomai.transMenus.collapsibleMenuImages.width
                twistyImage.style.paddingRight = org.archomai.transMenus.collapsibleMenuImages.space;
            twistyImage.style.marginLeft = "-"+org.archomai.transMenus.collapsibleMenuImages.moveLeft;
            triggerElement.insertBefore(twistyImage, triggerElement.firstChild)
                if (twistyImage.style.cursor) twistyImage.style.cursor = "pointer";
            twistyImage.subMenu = ListArray[i].id;
            if (org.archomai.transMenus.Persist.isExpanded(ListArray[i].id)) {
                twistyImage.setAttribute('src', org.archomai.transMenus.collapsibleMenuImages.openImage);
            } else {
                twistyImage.setAttribute('src', org.archomai.transMenus.collapsibleMenuImages.closedImage);
            }
            if (twistyImage.addEventListener) {
                twistyImage.addEventListener("click",org.archomai.transMenus.ExpandMenu,false);
            } else if (twistyImage.attachEvent) {
                twistyImage.attachEvent("onclick",org.archomai.transMenus.ExpandMenu);
            }
        } else continue;
    }
    if (org.archomai.transMenus.collapsibleMenuImages.closedImage) {
        var lImgCl = new Image();
        lImgCl.src = org.archomai.transMenus.collapsibleMenuImages.closedImage;
        var lImgOp = new Image();
        lImgOp.src = org.archomai.transMenus.collapsibleMenuImages.openImage;
    }
    org.archomai.transMenus.setupMovingHighlight();
    org.archomai.transMenus.initHighlight();
} ;
org.archomai.transMenus.SetStylesheet = function()
{
    var sheets = document.getElementsByTagName("link");
    for (var i=0;i<sheets.length;i++) {
        if (sheets[i].getAttribute("REL").toUpperCase().indexOf("STYLE")>-1 &&
                sheets[i].getAttribute("TITLE").toUpperCase().indexOf("DEFAULT")>-1) {
            sheets[i].disabled = true;
        } else if (sheets[i].getAttribute("REL").toUpperCase().indexOf("ALT")>-1 &&
                sheets[i].getAttribute("TITLE").toUpperCase().indexOf("EXTENDED")>-1) {
            if (document.all) {
                var link = document.createElement('link');
                link.rel = "stylesheet";
                link.type = "text/css";
                link.href = sheets[i].getAttribute("HREF");
                var head = document.getElementsByTagName('head')[0];
                head.appendChild(link);
            } else {
                sheets[i].disabled = false;
            }
        }
    }
};
if (org.archomai.transMenus.standards)
{
    if (window.addEventListener) {
        window.addEventListener("load",org.archomai.transMenus.MenuSetup,true);
    } else if (window.attachEvent){
        window.attachEvent("onload",org.archomai.transMenus.MenuSetup);
    }
} 
