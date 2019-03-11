(function () {
    window.amGloble = {
        Remind: function (d, text, key, dom) {    // d:数据，text：数据中的文本，key：数据中的唯一标识（id），dom：插入DOM节点的id名
            var checkData = JSON.parse(localStorage.getItem('checkData'));
            if (JSON.stringify(checkData) == 'null') {
                checkData = {};
            };
            var html = '';
            for (i = 0, l = d.length; i < l; i++) {
                var isChecked = false;
                var isOwn = checkData.hasOwnProperty(d[i][key]);   // 判断是否包含这个属性
                if (isOwn) {       // 如果包含这个订单属性，则取localStorage中的值
                    isChecked = checkData[d[i][key]];
                } else {           // 初始化都为false
                    checkData[d[i][key]] = false;    // localStorage没有此订单查看状态，则赋值fasle未查看
                    localStorage.setItem('checkData', JSON.stringify(checkData));       // 转为JSON字符串，存储localStorage  
                };

                var point = isChecked ? '' : '<div class="point"></div>';   // 已查看不显示红点，未查看就显示红点
                html += '<li><a href="./detail.html?key=' + d[i][key] + '&text=' + d[i].text + '"><span>' + d[i].text + point + '</span></a></li>';
            };
            $('#' + dom).html(html);
        },
        Updata: function (key) {
            if (key) {
                var checkData = JSON.parse(localStorage.getItem('checkData'));
                if (JSON.stringify(checkData) != 'null') {
                    checkData[key] = true;
                    localStorage.setItem('checkData', JSON.stringify(checkData));
                }
            };
        },
        GetQueryString: function (name) {
            // 获取地址栏参数
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null) return decodeURIComponent(r[2]); return null;
        }
    }
})();