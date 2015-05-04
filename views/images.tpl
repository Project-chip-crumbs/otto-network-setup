<html>
  <head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
  
  <!-- Core CSS file -->
  <link rel="stylesheet" href="assets/PhotoSwipe/photoswipe.css"> 

  <!-- Skin CSS file (styling of UI - buttons, caption, etc.)
  In the folder of skin CSS file there are also:
  - .png and .svg icons sprite, 
  - preloader.gif (for browsers that do not support CSS animations) -->
  <link rel="stylesheet" href="assets/PhotoSwipe/default-skin/default-skin.css"> 

  <!-- Core JS file -->
  <script src="assets/PhotoSwipe/photoswipe.min.js"></script> 

  <!-- UI JS file -->
  <script src="assets/PhotoSwipe/photoswipe-ui-default.min.js"></script> 
  <style type="text/css">
  .otto-logo{
    position: absolute;
    width: 14%;
    margin-left: 43%;
    z-index: 100;
  }
  </style>
  </head>

  <body>
<!-- Root element of PhotoSwipe. Must have class pswp. -->
<div class="pswp" tabindex="-1" role="dialog" aria-hidden="true">

    <!-- Background of PhotoSwipe. 
         It's a separate element as animating opacity is faster than rgba(). -->
    <div class="pswp__bg"></div>
    <div class="otto-logo"> <img src="assets/otto-logo-white.svg"/> </div>

    <!-- Slides wrapper with overflow:hidden. -->
    <div class="pswp__scroll-wrap">

        <!-- Container that holds slides. 
            PhotoSwipe keeps only 3 of them in the DOM to save memory.
            Don't modify these 3 pswp__item elements, data is added later on. -->
        <div class="pswp__container">
            <div class="pswp__item"></div>
            <div class="pswp__item"></div>
            <div class="pswp__item"></div>
        </div>

        <!-- Default (PhotoSwipeUI_Default) interface on top of sliding area. Can be changed. -->
        <div class="pswp__ui pswp__ui--hidden">

            <div class="pswp__top-bar">

                <!--  Controls are self-explanatory. Order can be changed. -->

                <div class="pswp__counter"></div>

                <button class="pswp__button pswp__button--share" title="Share"></button>

                <button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button>

                <button class="pswp__button pswp__button--zoom" title="Zoom in/out"></button>

                <!-- Preloader demo http://codepen.io/dimsemenov/pen/yyBWoR -->
                <!-- element will get class pswp__preloader-active when preloader is running -->
                <div class="pswp__preloader">
                    <div class="pswp__preloader__icn">
                      <div class="pswp__preloader__cut">
                        <div class="pswp__preloader__donut"></div>
                      </div>
                    </div>
                </div>
            </div>

            <div class="pswp__share-modal pswp__share-modal-hidden pswp__single-tap">
                <div class="pswp__share-tooltip"></div> 
            </div>

            <button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)">
            </button>

            <button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)">
            </button>

            <div class="pswp__caption">
                <div class="pswp__caption__center"></div>
            </div>

        </div>

    </div>

    <div class="container" style="text-align:right; position:absolute; bottom:15px; right:5px;">
      <div style="margin-left:10px; font-size:14pt;" class="glyphicon glyphicon-picture">          </div>
      <a href="/setup" style="margin-left:10px; font-size:14pt;"><div class="glyphicon glyphicon-cog">      </div></a>
      <a href="http://nextthing.co/otto.html" style="margin-left:10px; font-size:14pt;"><div class="glyphicon glyphicon-question-sign"></div></a>
      </ul>
    </div>
 
</div>

  <script>
    pswpElement = document.querySelectorAll('.pswp')[0];

    // build items array
    var items = [
% for file in files:
        { src: '{{file}}', w: 640, h: 480 },
% end
    ];
    
    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        escKey: false,
        pinchToClose: false,
        closeOnScroll: false,
        closeOnVerticalDrag: false,
        closeEl: false,
        tapToClose: false,
        modal: false,
        clickToCloseNonZoomable: false,
        indexIndicatorSep: " of ",
        index: 0, // start at first slide
        closeElClasses: [],
    };
    
    // Initializes and opens PhotoSwipe
    var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
    gallery.init();
  </script>
  </body>

</html>
