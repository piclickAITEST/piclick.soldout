function openModal(modalname){
    document.get
    $("#modal").fadeIn(300);
    $("."+modalname).fadeIn(300);
    $('body').addClass('stop-scrolling')
  }
  
  $(".close").on('click',function(){
    $("#modal").fadeOut(300);
    $(".modal-con").fadeOut(300);
    $('body').removeClass('stop-scrolling')
  });