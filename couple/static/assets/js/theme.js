// -----------------------------

//   JS INDEX
/* =================== */
/* 

    ## Animation Js
    ## Preloder
    ## Stiky menu
    ## Scrool Menu
    ## Scrool Up
    ## smart menu
    ## smoothscroll 
    ## Owl Carousel 
    ## Timer Js
    ## Googel Map
    ## Ajax
    ## Recaptcha

*/


(function($) {
  "use strict"; 


/*Animation js*/
AOS.init({

  offset:     120,

  delay:      0,

  easing:     'ease',

  duration:   5000,

  disable:    false, // Condition when AOS should be disabled. e.g. 'mobile'

  once:       false,

  mirror:     false, // whether elements should animate out while scrolling past them

  startEvent: 'DOMContentLoaded'

});








//**================== Preloder========================*//
$(window).on('load', function() {
  $('#preloader').fadeOut('slow', function() { $(this).remove(); });
});

//**================= End of Preloder =====================**//


//**================= Sticky =====================**//

 $(window).on('scroll', function() {
  if ($(window).scrollTop() > 250) {
      $('.aubliy-nav').addClass('nav-fixed');
      $('.header-area2').addClass('nav-fixed');
      $('.scroll-to-target').addClass('open');
  } else {
      $('.header-area2').removeClass('nav-fixed');
      $('.aubliy-nav').removeClass('nav-fixed');
      $('.scroll-to-target').removeClass('open');
  }
});
 


//**===================Scroll UP ===================**//

if ($('.scroll-to-target').length) {
  $(".scroll-to-target").on('click', function () {
    var target = $(this).attr('data-target');
    // animate
    $('html, body').animate({
      scrollTop: $(target).offset().top
    }, 1000);

  });
} 

//**===================Scroll UP ===================**//


//**================= End Smart Menu =====================**//


    /*---------------------
    smooth scroll
    --------------------- */
    $('.smoothscroll').on('click', function(e) {
      e.preventDefault();
      var target = this.hash;

      $('html, body').stop().animate({
          'scrollTop': $(target).offset().top - 150
      }, 3000);
  });


  /*---------------------
  
/*---------------------
    Sidepanel JS
    --------------------- */
    $('.sidebar-btn').on('click', function() {

      $('.side-panel').removeClass('hide');
  });

  $('.close-sp').on('click', function() {
      $('.side-panel').addClass('hide');
  });



    /*================================

    Magnific Popup

    ==================================*/

   $('.expand-img').magnificPopup({

      type: 'image',

      gallery: {

          enabled: true

      }

  }); 



  $('.expand-video').magnificPopup({

      type: 'iframe',

      gallery: {

          enabled: true

      }

  });



//**================== Owl Carousl========================*//

if ($('.blog-slider').length > 0) {   

  $('.blog-slider').owlCarousel({
  
    loop:true,
    margin:30,
    center:true,
    dots:false,
    nav:true,
    autoplay:false,
    autoplayTimeout:3000,
    /* navText:["<i class='flaticon-left'></i>","<i class='flaticon-right'></i>"], */
    smartSpeed :3000,
    responsive:{
        0:{
            items:1
        },
        450:{
            items:1
            },
        600:{
            items:1
            },
        1000:{
            items:1
        }
    }
  })
  }

  if ($('.hero-slider').length > 0) {   

    $('.hero-slider').owlCarousel({
    
      loop:true,
      margin:0,
      center:true,
      dots:false,
      nav:true,
      autoplay:false,
      autoplayTimeout:3000,
      navText:["<i class='flaticon-left-arrow'></i>","<i class='flaticon-right-2'></i>"],
      smartSpeed :3000,
      responsive:{
          0:{
              items:1
          },
          450:{
              items:1
              },
          600:{
              items:1
              },
          1000:{
              items:1
          }
      }
    })
    
    }


  if ($('.plant-slider').length > 0) {   

    $('.plant-slider').owlCarousel({
    
      loop:true,
      margin:10,
      center:true,
      dots:false,
      nav:true,
      autoplay:false,
      autoplayTimeout:3000,
      /* navText:["<i class='flaticon-left'></i>","<i class='flaticon-right'></i>"], */
      smartSpeed :3000,
      responsive:{
          0:{
              items:1
          },
          450:{
              items:1
              },
          600:{
              items:1
              },
          1000:{
              items:1
          }
      }
    })
    }
    if ($('.blog-detail-slider').length > 0) {   

      $('.blog-detail-slider').owlCarousel({
      
        loop:true,
        margin:30,
        center:false,
        dots:false,
        nav:true,
        autoplay:false,
        autoplayTimeout:3000,
        smartSpeed :3000,
        responsive:{
            0:{
                items:1
            },
            450:{
                items:1
                },
            600:{
                items:2
                },
            1000:{
                items:2
            }
        }
      })
      
      }
  

//**================== Owl Carousl========================*//

//Timer Js//

if ($('body').find('#clockdiv').length !== 0) {

  function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
      'total': t,
      'days': days,
      'hours': hours,
      'minutes': minutes,
      'seconds': seconds
    };
  }
  
  function initializeClock(id, endtime) {
    var clock = document.getElementById(id);
    var daysSpan = clock.querySelector('.days');
    var hoursSpan = clock.querySelector('.hours');
    var minutesSpan = clock.querySelector('.minutes');
    var secondsSpan = clock.querySelector('.seconds');
  
    function updateClock() {
      var t = getTimeRemaining(endtime);
  
      daysSpan.innerHTML = t.days;
      hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
      minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
      secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);
  
      if (t.total <= 0) {
        clearInterval(timeinterval);
      }
    }
  
    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
  }
  var deadline = new Date("Sep5, 2020 19:37:25"); 
  initializeClock('clockdiv', deadline);
} 

//**=================End Timer=====================**//





}(jQuery));
  


//**=================== Google Map ==========================**//

if ($('#googleMap').length > 0) { 
  var user_lat, user_lng;
      var map;
  
      function initMap() {
          map = new google.maps.Map(document.getElementById('googleMap'), {
              center: {
                  lat: 23.782062,
                  lng: 90.416053
              },
              zoom: 15,
              scrollwheel: false
          });
                
        var marker = new google.maps.Marker({
          position:  {  lat: 23.782062, lng: 90.416053},
          map: map,
       /*    icon: "window/img/locator.png" */
        });
  
            } 
          }
  
  //*================ End Google Map ============*//
  
/*---------------------
    // Ajax Contact Form
    --------------------- */

    $('.cf-msg').hide();
    $('form#cf button#submit').on('click', function() {
    
        var name = $('#name').val();
        var email = $('#email').val();
        var subject = $('#subject').val();
        var msg = $('#msg').val();2
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    
        if (!regex.test(email)) {
            alert('Please enter valid email');
            return false;
        }
    
        name = $.trim(name);
        email = $.trim(email);
        msg = $.trim(msg);
    
        if (name != '' && email != '' && subject != '' && msg != '') {
            var values = "name=" + name + "&email=" + email + "&subject=" + subject + "&msg=" + msg;
            $.ajax({
                type: "POST",
                url: "assets/mail-sender/contact.php",
                data: values,
                success: function() {
                    $('#name').val('');
                    $('#email').val('');
                    $('#subject').val('');
                    $('#msg').val('');
    
                   $('.cf-msg').fadeIn().html('<div class="alert alert-success"><strong>Success!</strong> Email has been sent successfully.</div>');
                    setTimeout(function() {
                        $('.cf-msg').fadeOut('slow');
                    }, 4000);
                }
            });
        } else {
            $('.cf-msg').fadeIn().html('<div class="alert alert-danger"><strong>Warning!</strong> Please fillup the informations correctly.</div>')   
            $('.cf-msg').fadeOut(2000)
        }
        return false;
    });


// Ajax Contact Form JS END


