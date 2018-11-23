//import moment from 'moment';
var moment = require('moment');
// import * as moment from 'moment';



function PrefixInteger(num, length) {
    return ("0000000000000000" + num).substr(-length);
}

// Date.prototype.format = function (format) {
//     var o = {
//         "M+": this.getMonth() + 1,
//         "d+": this.getDate(),
//         "h+": this.getHours(),
//         "m+": this.getMinutes(),
//         "s+": this.getSeconds(),
//         "q+": Math.floor((this.getMonth() + 3) / 3),
//         "S": this.getMilliseconds()
//     }
//     if (/(y+)/.test(format)) {
//         format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
//     }
//     for (var k in o) {
//         if (new RegExp("(" + k + ")").test(format)) {
//             format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
//         }
//     }
//     return format;
// }

/** 
        date 为long类型
        pattern 为格式化参数 
*/
//function getFormatDate(date, pattern) {
const getFormatDate = (date, pattern) => {    
    if (date == undefined) {
        date = new Date();
    }
    if (pattern == undefined) {
        pattern = "yyyy-MM-dd hh:mm:ss";
    }
    return date.format(pattern);
}

const getFstDateStr = (dt) => {
    let now = new Date()
    if (!dt)
        now = dt
    let dateStr = getFormatDate(now, 'yyyy-MM-dd');
    //console.log('getHours:', now.getHours()  )
    if (now.getHours() >= 21) {
        let tomo = new Date()
        tomo.setTime(tomo.getTime() + 24 * 60 * 60 * 1000);
        dateStr = getFormatDate(tomo, 'yyyy-MM-dd');
    }
    //console.log('dateStr:', dateStr )
    return dateStr
};

const getDateStr = (dt) => {//如果是21点前， 返回当日日期，如果是21点后， 返回明天日期 

    let now = new Date()
    if (!dt)
        now = dt
    let dateStr = '' //PrefixInteger( now.getYear() , 4 ) +'-'+PrefixInteger( now.getMonth() , 2 )+'-'+PrefixInteger( now.getDate() , 2 );  //now.Format("yyyy-MM-dd")
    dateStr = getFormatDate(now, 'yyyy-MM-dd');
    return dateStr
};

const getTimeStr = (dt) => {
    let now = new Date()
    if (!dt)
        now = dt
    let timeStr = ''

    timeStr = getFormatDate(now, 'hh:mm:ss');
    return timeStr
};

//获取晚上21:00~23：30 分钟列表
const get21TimeList = () => {
    let dt = moment()
    dt.set('hour', 9)
    dt.set('minute', 0)
    dt.set('second', 0)
    return dt.format('hh:mm:ss');
};

const testFun = () => {
    console.log('test():', get21TimeList() );
};

// module.exports.getDateStr = getDateStr;
// module.exports.getFstDateStr = getFstDateStr;
//module.exports.getFormatDate = getFormatDate;

module.exports.testFun = testFun;

