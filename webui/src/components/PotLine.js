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
import { array } from 'prop-types';


 

 
class PotLine extends Component {


    constructor(props) {
        super(props);
        this.state = {
            code:'002415',
            datalist: null,
            minClose:0, maxClose:0,
            width: 1000, height: 600
        };

    }

    componentWillMount() {
        console.log("PotLine componentWillMount "  )
      
 
 
    }

    componentDidMount() {
        console.log("PotLine DidMount ")
        // window.addEventListener('resize', this.resize);

        
        console.log('this.props.code :', this.props.code  )
        this.state.code = this.props.code;

        // 基于准备好的dom，初始化echarts实例
        let tempMyChart = echarts.init(document.getElementById('potline_form'));
        this.setState({ myChart: tempMyChart , code: this.props.code })
 
        
        this.updateFstchart()
        setInterval(() => {  
            this.getPotdata( this.state.code )
            
        }, 60000 );
        setTimeout(() => {  
            this.getPotdata( this.state.code )
            
        }, 1000 );

    }

    componentWillUnmount() {
        // window.removeEventListener('resize', this.resize);
 
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
                height = width * 0.60;
            }
            this.setState({ width, height });
            this.state.myChart.resize();

        } catch (ignore) {
        }
    }

    getPotdata =(code) =>{
 
        //stock/potdata/600177
        let dataUrl = '/stock/potdata/' + code
        request(dataUrl).then(data => {
            console.log('request : ' + dataUrl  )
            console.log('respone :',data)
            if (data.data) {
                console.log('respone :',data)
                let potdata = data.data 
                // let temp = this.apidata2uidata_signal(data.data.data)
                // this.state.datalist_goodpot = temp
                // this.state.updateState = true
                this.state.datalist = potdata;
                this.setState({ datalist: potdata });
                console.log('respone :',potdata)

            }
        })        

    }
    

    updateFstchart = () => {
        console.log('updatechart:')

        let dataSrc = [{"dim": 0.17, "minclose": 8.71, "type": 1, "tickcount": 14, "datetime": "2019-02-25 13:55:00", "volume": 104779, "datatype": "pot", "time": "", "date": "", "close": 8.78, "endtime": "", "open": 8.57, "vtSymbol": ""}, {"dim": -0.19, "minclose": 8.65, "type": -1, "tickcount": 1, "datetime": "2019-02-26 09:35:00", "volume": 25602, "datatype": "pot", "time": "", "date": "", "close": 8.59, "endtime": "", "open": 8.78, "vtSymbol": ""}, {"dim": 0.17, "minclose": 8.69, "type": 1, "tickcount": 2, "datetime": "2019-02-26 09:40:00", "volume": 33449, "datatype": "pot", "time": "", "date": "", "close": 8.76, "endtime": "", "open": 8.59, "vtSymbol": ""} ]

        //let dtlist=new Array()
        let dtlist = []
        let closelist = new Array()
        let mincloselist = new Array()
        
        
        dataSrc = this.state.datalist
        
        console.log( 'update chart：', dataSrc );
        if( dataSrc !=null ){
            for( let rec of dataSrc ){
                console.log( rec );
                dtlist.push(  rec.datetime )
                closelist.push(  rec.close )
                mincloselist.push(  rec.minclose )
            }
        }
        console.log( 'dtlist:', mincloselist );
        console.log( 'dtlist:', closelist );

        if( closelist.length >0 ){
            let tempMin = closelist[0] * 0.99
            let tempMax = closelist[0] * 1.01
            if (Math.max.apply(null, closelist) * 1.005 > tempMax) {
                tempMax = Math.max.apply(null, closelist) * 1.005
            }
            if (Math.min.apply(null, closelist) * 0.995 < tempMin) {
                tempMin = Math.min.apply(null, closelist) * 0.995
            }

            this.state.maxClose = (tempMax).toFixed(2)
            this.state.minClose = (tempMin).toFixed(2)  
        }


        let option = {
            title: {
                text: '点差图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['点差','最后收盘价' ]
            },

   
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: dtlist //['周一','周二','周三','周四','周五','周六','周日']
            },
            yAxis: {
                type: 'value',
                min: this.state.minClose,  
                max: this.state.maxClose                  
            },
            series: [
                {
                    name:'点差',
                    type:'line',
                    //stack: '总量',
                    data:closelist //[120, 132, 101, 134, 90, 230, 210]
                },
                {
                    name:'最后收盘价',
                    type:'line',
                    //stack: '总量',
                    data:mincloselist//[220, 182, 191, 234, 290, 330, 310]
                }
 
            ]
        };        
 

        console.log('will setOption ')
        console.log('this.state.myChart is  ', this.state.myChart)

        // 绘制图表
        if (this.state.myChart != null) {
            this.state.myChart.setOption(option);

        }

    }

    getdata = (code, date) => {
        // this.getMinData(code, date);
        // this.getGoodPotData(code, date);
        // this.getPotData(code,date);

    }

    

 

    render() {
        console.log('potline render() ', this.state.code  )
 
        this.state.isResize = false;
        this.updateFstchart()
        //width :-1,  height:-1
        //console.log('this.state.width:', this.state.width )
        return (
            <div id="potline_form" style={{ width: this.state.width, height: this.state.height }}></div>
        );
    }

}


PotLine.defaultProps = { code: '002415' 
 }

export default PotLine;


