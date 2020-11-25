// 스크롤 높이 핸들링
function handleScroll() {
    var height = $(document).innerHeight() - $(window).innerHeight();
    var currPosition = $(window).scrollTop();
    if (height * 0.5 < currPosition) { 
        $('.btn-list').removeAttr("hidden")
    }
}

// 쓰로틀 적용 스크롤 이벤트
$(window).scroll($.throttle(150, function () {
        handleScroll()
    })
)