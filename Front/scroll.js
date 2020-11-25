// 스크롤 높이 핸들링
function handleScroll() {
    var height = $(document).innerHeight() - $(window).innerHeight();
    var currPosition = $(window).scrollTop();

    // 스크롤이 특정 위치에 도달 했을 경우에만 표시
    // height * 0.5 < currPosition ? $('.btn-list').removeAttr("hidden") : $('.btn-list').attr("hidden", "")

    // 스크롤 위치가 50% 달성 시 무조건 표시
    if (height * 0.5 < currPosition) { 
        $('.btn-list').removeAttr("hidden")
    }
}

// 쓰로틀 적용 스크롤 이벤트
$(window).scroll($.throttle(150, function () {
        handleScroll()
    })
)

// 쓰로틀 제거 스크롤 이벤트
// $(window).scroll(function () {
//         handleScroll()
//     }
// )