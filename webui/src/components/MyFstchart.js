import React, { Component } from 'react';
import ReactDOM from 'react-dom';

// 引入 ECharts 主模块
import echarts from 'echarts/lib/echarts';
// 引入柱状图
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/line';
import 'echarts/lib/chart/scatter';
import 'echarts/lib/chart/candlestick';


// 引入提示框和标题组件
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/axis';
import 'echarts/lib/component/markLine';
import request from '../utils/request'


Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

function getDateStr() {   //如果是21点前， 返回当日日期，如果是21点后， 返回明天日期
    let now = new Date()
    let dateStr = now.Format("yyyy-MM-dd")
    //console.log('getHours:', now.getHours()  )
    if (now.getHours() >= 21) {
        let tomo = new Date()
        tomo.setTime(tomo.getTime() + 24 * 60 * 60 * 1000);
        dateStr = tomo.Format("yyyy-MM-dd")
    }
    //console.log('dateStr:', dateStr )
    return dateStr
}

class MyFstchart extends Component {


    constructor(props) {
        super(props);
        this.state = {
            datelist: [], datalist: [],
            datalist_goodpot: [],
            datalist_pot:[],
            myChart: null, updateState: false, isResize: false,
            minClose: 0, maxClose: 0, baseClose: 0,
            idInterval: 0,
            width: 1000, height: 640
        };

    }

    componentWillMount() {
        console.log("MyFstchart componentWillMount ")

        this.state.isResize = false;
        this.getdata(this.props.code, this.props.date)
        setTimeout(() => {
            //this.setState({ myChart: tempMyChart })
            this.setState({ datelist: this.state.datelist, datalist: this.state.datalist });
        }, 2000);


    }

    componentDidMount() {
        console.log("MyFstchart DidMount ")
        window.addEventListener('resize', this.resize);

        //this.getdata( this.props.code )

        // 基于准备好的dom，初始化echarts实例
        let tempMyChart = echarts.init(document.getElementById('fst_form'));
        this.setState({ myChart: tempMyChart })
        this.updateFstchart()

        this.state.idInterval = setInterval(() => {
            this.getdata(this.props.code, this.props.date)
        }, 5000)

    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.resize);
        clearInterval(this.state.idInterval)
        this.state.idInterval = 0
    }

    resize = () => {
        console.log('resize() ')
        this.state.isResize = true
        try {
            const parentDom = ReactDOM.findDOMNode(this).parentNode;
            let { width, height } = this.props;
            //如果props没有指定height和width就自适应
            if (!width) {
                width = parentDom.offsetWidth;
            }
            if (!height) {
                height = width * 0.64;
            }
            this.setState({ width, height });
            this.state.myChart.resize();

        } catch (ignore) {
        }
    }

    updateFstchart = () => {
        console.log('updateFstchart:')

        let option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['分时线', '信号']
            },
            toolbox: {
                show: true,
                feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false },
                    magicType: { show: true, type: ['line', 'bar', 'stack', 'tiled'] },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            calculable: true,
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: this.state.datelist
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    min: this.state.minClose,  //this.state. tempMin
                    max: this.state.maxClose      // *1.005
                }
            ],
            series: [

                {
                    name: '分时线',
                    type: 'line',
                    symbol: 'emptyCircle',
                    itemStyle: {
                        normal: {
                            lineStyle: {            // 系列级个性化折线样式，横向渐变描边
                                width: 2,
                                color: 'orange',
                                shadowColor: 'rgba(0,0,0,0.5)',
                                shadowBlur: 10,
                                shadowOffsetX: 8,
                                shadowOffsetY: 8
                            }
                        },
                        emphasis: {
                            label: { show: true }
                        }
                    },

                    data: this.state.datalist,
                    markLine: {//标记线设置
                        lineStyle: {
                            normal: {
                                type: 'solid'
                            }
                        },
                        symbolSize: 0,//控制箭头和原点的大小、官方默认的标准线会带远点和箭头
                        data: [
                            {
                                name: 'Y 轴值为 -1% 的水平线',
                                yAxis: (this.state.baseClose * 0.99).toFixed(2)
                            },
                            {
                                name: 'Y 轴值为 baseClose 的水平线',
                                yAxis: (this.state.baseClose * 1.00).toFixed(2)
                            },
                            {
                                name: 'Y 轴值为 +1% 的水平线',
                                yAxis: (this.state.baseClose * 1.01).toFixed(2)
                            },

                            // [
                            //     { name: '标线1起点', value: 11050, xAxis:'09:08:00', yAxis: 11050 },      // 当xAxis为类目轴时，数值1会被理解为类目轴的index，通过xAxis:-1|MAXNUMBER可以让线到达grid边缘
                            //     { name: '标线1终点', xAxis:'14:37:00' , yAxis: 11050 },             //   xAxis: MAXNUMBER,
                            // ]
                        ]
                    }


                },
                {
                    name: 'goodpot',
                    type: 'scatter',
                    // 数据格式  [['14:00:00',11300],['14:15:00',11350] ]
                    data: this.state.datalist_goodpot

                }

            ]
        };

        let series_pot = {
            name: 'potline',
            type: 'line',
            // 数据格式  [['14:00:00',11300],['14:15:00',11350] ]
            data: this.state.datalist_pot
        }
        if (this.props.showPot == true) {
            option.series.push(series_pot) 
        }


        // 绘制图表
        if (this.state.myChart != null) {
            this.state.myChart.setOption(option);

        }

    }

    getdata = (code, date) => {
        this.getMinData(code, date);
        this.getGoodPotData(code, date);
        this.getPotData(code,date);

    }

    getMinData = (code, date) => {
        //let strDate = (new Date()).Format("yyyy-MM-dd")  // Format("yyyy-MM-dd hh:mm:ss.S")  ==>  2006-07-02 08:09:04.423 
        let strDate = date
        let dataUrl = '/future/minline/' + this.props.code + '/' + strDate
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl + '  ' + this.props.code)
            if (data.data) {

                let kdata = data.data.data

                let temp = this.apidata2uidata(data.data.data)
                if (temp[1].length <= 0)
                    return;
                let tempMin = temp[1][0] * 0.99
                let tempMax = temp[1][0] * 1.01
                if (Math.max.apply(null, temp[1]) * 1.005 > tempMax) {
                    tempMax = Math.max.apply(null, temp[1]) * 1.005
                }
                if (Math.min.apply(null, temp[1]) * 0.995 < tempMin) {
                    tempMin = Math.min.apply(null, temp[1]) * 0.995
                }
                this.state.baseClose = temp[1][0]
                this.state.datelist = temp[0]
                this.state.datalist = temp[1]
                this.state.maxClose = (tempMax).toFixed(2)
                this.state.minClose = (tempMin).toFixed(2)
                this.state.updateState = true
                this.setState({ datelist: temp[0], datalist: temp[1] });

                //   setTimeout( ()=>{
                //     this.setState({ datelist:temp[0] , datalist:temp[1]  } );   
                //   }, 500 )
            }
        })
    }

    getGoodPotData = (code, date) => {
        //let strDate = (new Date()).Format("yyyy-MM-dd")  // Format("yyyy-MM-dd hh:mm:ss.S")  ==>  2006-07-02 08:09:04.423      
        let strDate = date
        let dataUrl = '/future/signal/' + this.props.code + '/' + strDate
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl + '  ' + this.props.code)
            if (data.data) {

                let kdata = data.data.data
                let temp = this.apidata2uidata_signal(data.data.data)
                this.state.datalist_goodpot = temp
                this.state.updateState = true
                this.setState({ datalist_goodpot: temp });

            }
        })
    }


    getPotData = (code, date) => {
        //let strDate = (new Date()).Format("yyyy-MM-dd")  // Format("yyyy-MM-dd hh:mm:ss.S")  ==>  2006-07-02 08:09:04.423      
        let strDate = date
        let dataUrl = '/future/exdata/pot/' + this.props.code + '/' + strDate
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl + '  ' + this.props.code)
            if (data.data) {

                let kdata = data.data.data
                let temp = this.apidata2uidata_pot(data.data.data)
                console.log('getGoodPotData:', temp)
 
                this.state.datalist_pot = temp
                this.state.updateState = true
                this.setState({ datalist_pot: temp });
                
            }
        })
    }

   

    apidata2uidata = (mindata) => {
        let dateList = [];
        let dataList = [];
        for (let i = 0; i < mindata.length; i++) {
            let rec = mindata[i]
            dateList.push(rec.time.substr(0, 8))
            dataList.push(rec.close)
        }

        return [dateList, dataList]
    }

    apidata2uidata_signal = (signaldata) => {

        let dataList = [];
        for (let i = 0; i < signaldata.length; i++) {
            let rec = signaldata[i]
            dataList.push([rec.time.substr(0, 5) + ':00', rec.lastPrice])
        }

        return dataList
    }

    apidata2uidata_pot =(potdata) =>{
        let dataList = [];
        for (let i = 0; i < potdata.length; i++) {
            let rec = potdata[i]
            dataList.push([rec.time.substr(0, 5) + ':00', rec.close])
        }

        return dataList
    }


    render() {
        console.log('MyFstchart render() ')

        if (this.state.updateState == true) {
            this.state.updateState = false
        } else {
            if (this.state.isResize == false) {
                this.getdata(this.props.code, this.props.date)
            }
        }
        this.state.isResize = false;
        this.updateFstchart()
        //width :-1,  height:-1
        //console.log('this.state.width:', this.state.width )
        return (
            <div id="fst_form" style={{ width: this.state.width, height: this.state.height }}></div>
        );
    }

}


MyFstchart.defaultProps = {
    code: 'RU0',
    date: getDateStr(),
    showPot: true

}

export default MyFstchart;


