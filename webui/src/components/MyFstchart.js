import React, { Component } from 'react';

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

import request from '../utils/request'


class MyFstchart extends Component {

    constructor(props) {
        super(props);
        this.state = { date: new Date(),
            datelist: [], datalist: [], 
            datalist_goodpot:[],
            myChart: null, updateState: false,
            minClose:0, maxClose:0 };
    }

    componentWillMount() {
        console.log("MyFstchart componentWillMount ")
        this.getdata(this.props.code)
        setTimeout(() => {
            //this.setState({ myChart: tempMyChart })
            this.setState({ datelist :this.state.datelist , datalist:this.state.datalist });
        }, 2000 );
    }

    componentDidMount() {
        console.log("MyFstchart DidMount ")
        //this.getdata( this.props.code )

        // 基于准备好的dom，初始化echarts实例
        let tempMyChart = echarts.init(document.getElementById('fst_form'));
        this.setState({ myChart: tempMyChart })
        this.updateFstchart()
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
                    min: this.state.minClose*0.995,  //this.state.
                    max: this.state.maxClose*1.005
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
                    data: this.state.datalist
                    
                    // [
                    //     620, 732, 791,
                    //     { value: 734, symbol: 'emptyHeart', symbolSize: 10 },
                    //     890, 930, 820
                    // ]

                },
                {
                    name:'goodpot',
                    type:'scatter',
                    // 数据格式  [['14:00:00',11300],['14:15:00',11350] ]
                    data: this.state.datalist_goodpot 
 
                },
                
            ]
        };


        // 绘制图表
        if (this.state.myChart != null)
            this.state.myChart.setOption(option);

    }

    getdata = (code ,date ) => {
        this.getMinData( code, date );
        this.getGoodPotData( code, date );

    }

    getMinData =( code, date) =>{
        let strDate = (new Date()).Format("yyyy-MM-dd")  // Format("yyyy-MM-dd hh:mm:ss.S")  ==>  2006-07-02 08:09:04.423 
        let dataUrl = '/future/minline/' + this.props.code + '/' +strDate
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl + '  ' + this.props.code)
            if (data.data) {

                let kdata = data.data.data

                let temp = this.apidata2uidata(data.data.data)
                this.state.datelist = temp[0]
                this.state.datalist = temp[1]
                this.state.maxClose = Math.max.apply(null,temp[1]);
                this.state.minClose = Math.min.apply(null,temp[1]);
                this.state.updateState = true
                this.setState({ datelist: temp[0], datalist: temp[1] });

                //   setTimeout( ()=>{
                //     this.setState({ datelist:temp[0] , datalist:temp[1]  } );   
                //   }, 500 )
            }
        })
    }

    getGoodPotData =( code, date) =>{
        let strDate = (new Date()).Format("yyyy-MM-dd")  // Format("yyyy-MM-dd hh:mm:ss.S")  ==>  2006-07-02 08:09:04.423      
        let dataUrl = '/future/signal/' + this.props.code+   '/' +strDate    
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl + '  ' + this.props.code)
            if (data.data) {

                let kdata = data.data.data
                let temp = this.apidata2uidata_signal(data.data.data)
                // console.log(temp)
                // temp  = [['14:00:00',11270],['14:15:00',11250] ]
                // console.log(temp)
                this.state.datalist_goodpot = temp
                this.state.updateState = true
                this.setState({ datalist_goodpot: temp });

                console.log('getGoodPotData:',  temp )

                //   setTimeout( ()=>{
                //     this.setState({ datelist:temp[0] , datalist:temp[1]  } );   
                //   }, 500 )
            }
        })        
    }

    apidata2uidata = (mindata) => {
        let dateList = [];
        let dataList = [];
        for (let i = 0; i < mindata.length; i++) {
            let rec = mindata[ i ]
            dateList.push(rec.time.substr(0,8))
            dataList.push( rec.close )
        }

        return [dateList, dataList]
    }

    apidata2uidata_signal = (signaldata) => {
  
        let dataList = [];
        for (let i = 0; i < signaldata.length; i++) {
            let rec = signaldata[ i ]            
            dataList.push( [rec.time.substr(0,5)+':00' , rec.lastPrice ] )
        }

        return dataList
    }    
 

    render() {
        console.log('MyFstchart render() ')

        if (this.state.updateState == true) {
            this.state.updateState = false
        } else {
            this.getdata(this.props.code)
        }
        this.updateFstchart()
        return (
            <div id="fst_form" style={{ width: 1024, height: 700 }}></div>
        );
    }

}

MyFstchart.defaultProps = {
    code: 'RU0'
}

export default MyFstchart;


Date.prototype.Format = function (fmt) { //author: meizz 
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