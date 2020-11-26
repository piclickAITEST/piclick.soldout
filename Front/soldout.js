const siteID = 149;
const au_id = 2605;
const productID = 6260;
const product_set_id = 'AIPIC_KR';
const contentUrl = '//shescloset.com/web/product/big/202010/0ae275caf55270643fd916de7588da16.jpg';
const uID = '1379024132.1604381524';
const userID = 'wlsdn2215';
const pKey = siteID + "_" + au_id

// 화폐 전환
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// 유사 상품 추천
const similarSearch = function() {
  $.ajax({
    type: "GET",
    url: 'https://sol.piclick.kr/similarSearch/'+ au_id +'/' +siteID + '_' + productID + '?contentUrl=' + contentUrl + '&product_set_id=' + product_set_id + '&banner=True',
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    timeout: 30000,
    success: function(json) {
      // console.log(json)
      var item = $('.ai-reco #item').clone();
      $('.ai-reco #item').remove();
      if (json.status == 'S') {
        $.each(json.result, function(idx, dict) {
          var $item = item.clone();
          $('img', $item).attr('src', dict.img_url);
          $('a', $item).attr('href', dict.click_url);
          $('#tag', $item).attr('src', dict.p_key);
          $('#product_name', $item).text(dict.product_name);
          $('#product_price', $item).text(numberWithCommas(dict.product_price) + '원');
          $('.ai-reco #items').append($item);
        })
      }
    },
    error: function(e) {
      console.log(e)
    }
  })
}

// 개인화 추천
const userSearch = function () {
  $.ajax({
    type: "GET",
    url: 'https://sol.piclick.kr/userSearch/cookie/' + au_id + '?uid=' + uID + '&user_id=' + userID,
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    timeout: 5000,
    success: function (json) {
      if (json.status == 'S') {
        var item = $('.p-reco #item').clone();
        $('.p-reco #item').remove();
        if (json.status == 'S') {
          $.each(json.result, function(idx, dict) {
            // clickList.push(dict.click_url);
            var $item = item.clone();
            $('img', $item).attr('src', dict.img_url);
            $('a', $item).attr('href', dict.click_url + '&site_id=' + siteID + '&device=m');
            $('#tag', $item).attr('src', dict.p_key);
            $('#product_name', $item).text(dict.product_name);
            $('#product_price', $item).text(numberWithCommas(dict.product_price) + '원');
            $('.p-reco #items').append($item);
          })
        }
      }
    }, error: function (e) {
      console.log(e)
    }
  })
}

// 유사 가격대 추천
const smaePrice = function () {
  $.ajax({
    type: "GET",
    url: 'https://sol.piclick.kr/soldoutSearch/similarPrice/' + au_id + '/' + pKey ,
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    timeout: 5000,
    success: function (json) {
      if (json.status == 'S') {
        var item = $('.same-price #item').clone();
        $('.same-price #item').remove();
        if (json.status == 'S') {
          $.each(json.result, function(idx, dict) {
            // clickList.push(dict.click_url);
            var $item = item.clone();
            $('img', $item).attr('src', dict.img_url);
            $('a', $item).attr('href', dict.click_url + '&site_id=' + siteID + '&device=m');
            $('#tag', $item).attr('src', dict.p_key);
            $('#product_name', $item).text(dict.product_name);
            $('#product_price', $item).text(numberWithCommas(dict.product_price) + '원');
            $('.same-price #items').append($item);
          })
        }
      }
    }, error: function (e) {
      console.log(e)
    }
  })
}

similarSearch();
userSearch();
smaePrice();
