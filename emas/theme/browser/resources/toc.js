////
// Additional Javascript to change Transmenus behavior for table of contents (vs collection composer)
// (we expect this to be called on load after transmenus is loaded, but before any of it is called)
////
// change default behavior from expanded to collapsed
org.archomai.transMenus.Persist.defaultExpanded = false
// change cookie name to avoid conflict with collection composer use
org.archomai.transMenus.Persist.cookiename = "table_of_contents"
// change the ToC twisty widget images to arrows
org.archomai.transMenus.collapsibleMenuImages =
{
    openImage : "++resource++rhaptos.compilation/downArrow.gif" ,
    closedImage : "++resource++rhaptos.compilation/rightArrow.gif",
    height : "9px",
    width : "9px",
    space : "0px",
    moveLeft : "13px"
}
// new namespace for new stuff
if (!org.archomai.transMenus.toc) {
    org.archomai.transMenus.toc= {};
}
// similar to ExpandMenu, make ToC headers clickable-expandable
org.archomai.transMenus.toc.ExpandMenuHeader = function(e)
{
    var eventTarget = (document.all) ? event.srcElement : e.target;
    var subMenu = eventTarget.parentNode.getElementsByTagName('ul')[0].id;
    if (subMenu) {
        org.archomai.transMenus.MenuRegistry[subMenu].HandleMouseDown();
        if (document.all) event.cancelBubble = true;
        if (e && !document.all) e.stopPropagation();
    }
} ;
// open (without persisting) all nodes containing the current section
// meant to be run onload
org.archomai.transMenus.toc.openCurrent = function(id) {
    // borrows closely from HandleMouseDown in TransMenus
    for (var x = 0; x < org.archomai.transMenus.highlight.length; x++) {
        var elt = document.getElementById(org.archomai.transMenus.highlight[x]);
        if (elt.style.display == 'none') { // hidden... open without persisting
            elt.parentNode.childNodes[2].className='cnx_chapter_header'; // undo cnx_current from initHighlight
            elt.style.display='block';
            elt.parentNode.firstChild.setAttribute('src', org.archomai.transMenus.collapsibleMenuImages.openImage);
            elt.gentle = 'true'; // IE flaky on .[set|remove|has]Attribute
        } // else: already open (due to cookie load state)... leave alone
    }
} ;
// on load, set the cookie if you don't have it already, so we can reduce ToC flicker
// (the template looks for a cookie as proof it can do at-render expand/contract)
org.archomai.transMenus.toc.initCookie = function(id) {
    if (org.archomai.transMenus.Persist.cookiename != null) {
        var allcookies = document.cookie;
        var pos = allcookies.indexOf(org.archomai.transMenus.Persist.cookiename + "=");
        if (pos == -1) { // no cookie
            org.archomai.transMenus.Persist.setState();
        }
    }
}
// onload operations for Table of Contents
org.archomai.transMenus.toc.tocInit = function(id) {
    org.archomai.transMenus.toc.openCurrent()
        //setTimeout('org.archomai.transMenus.toc.openCurrent()', 800); // "animation"
        org.archomai.transMenus.toc.initCookie();
}
// register onload events
if (org.archomai.transMenus.standards)
{
    if (window.addEventListener) {
        window.addEventListener("load",org.archomai.transMenus.toc.tocInit,true);
    } else if (window.attachEvent){
        window.attachEvent("onload",org.archomai.transMenus.toc.tocInit);
    }
} 
