import React, { Component } from 'react';

// 引入 ECharts 主模块
import echarts from 'echarts/lib/echarts';
// 引入柱状图
import  'echarts/lib/chart/bar';
import 'echarts/lib/chart/candlestick';
// 引入提示框和标题组件
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/axis';

import request from '../utils/request'
 
 
class MyKchart2 extends Component {

    constructor(props) {
        super(props);
        this.state = {date: new Date(), datelist:[], datalist:[], myChart:null, updateState :false };
    }
    
    componentWillMount(){
        console.log( "MyKchart2 componentWillMount " )
        this.getdata( this.props.code )
    }  
 
    componentDidMount() {
        console.log( "MyKchart2 DidMount " )
        //this.getdata( this.props.code )

        // 基于准备好的dom，初始化echarts实例
        let tempMyChart = echarts.init(document.getElementById('k_form'));
        this.setState({ myChart: tempMyChart})        
        this.updateKchart()
    }

    updateKchart =()=>{
        console.log('updateKchart:')

        let option = {
            tooltip : {
                trigger: 'axis',
                formatter: function (params) {  //rec.open, rec.close, rec.low, rec.high
                    var res = params[0].seriesName + ' ' + params[0].name;
                    res += '<br/>  开盘 : ' + params[0].value[1] + '  最高 : ' + params[0].value[4];
                    res += '<br/>  收盘 : ' + params[0].value[2] + '  最低 : ' + params[0].value[3];
                    return res;
                }
            },
            legend: {
                data:['上证指数']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataZoom : {show: true},
                    dataView : {show: true, readOnly: false},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            dataZoom : {
                show : true,
                realtime: true,
                start : 0,
                end : 50
            },
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : true,
                    axisTick: {onGap:false},
                    splitLine: {show:false},
                    data :   this.state.datelist   //dateList
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    scale:true,
                    boundaryGap: [0.01, 0.01]
                }
            ],
            series : [
                {
                    name:'价格走势', 
                    type:'candlestick',
                    barMaxWidth: 20,
                    itemStyle: {
                        normal: {
                            color: 'red',           // 阳线填充颜色
                            color0: 'lightgreen',   // 阴线填充颜色
                            lineStyle: {
                                width: 2,
                                color: 'orange',    // 阳线边框颜色
                                color0: 'green'     // 阴线边框颜色
                            }
                        },
                        emphasis: {
                            color: 'black',         // 阳线填充颜色
                            color0: 'white'         // 阴线填充颜色
                        }
                    },
                    data: this.state.datalist, //   dataList,
                    markPoint : {
                        symbol: 'star',
                        //symbolSize:20,
                        itemStyle:{
                            normal:{label:{position:'top'}}
                        },
                        data : [
                            {name : '最高', value : 2444.8, xAxis: '2013/2/18', yAxis: 2466}
                        ]
                    }
                }
            ]
        };
                            

        // 绘制图表
        if( this.state.myChart != null )
            this.state.myChart.setOption( option );

    } 

    getdata = ( code )=>{
        let dataUrl = '/future/kline/' + this.props.code 
 
        request( dataUrl ).then(data => { 
          console.log('request : '+ dataUrl  +'  '+ this.props.code )
          if( data.data ){  
            
              let kdata = data.data.data 
              
               let temp = this.apidata2uidata( data.data.data  )
               this.state.datelist = temp[0]
               this.state.datalist = temp[1]
               this.state.updateState  = true 
               this.setState({ datelist:temp[0] , datalist:temp[1]  } ); 

            //   setTimeout( ()=>{
            //     this.setState({ datelist:temp[0] , datalist:temp[1]  } );   
            //   }, 500 )
          }             
        })
    }
    
    apidata2uidata =( kdata ) =>{
        let dateList =[];
        let dataList =[];
        for (let i=0; i<kdata.length ;i++ ){
            let rec = kdata[kdata.length-1-i]
            dateList.push( rec.date )
            dataList.push( [rec.open, rec.close, rec.low, rec.high]    ) 
              
        }

        return [dateList,dataList]
    }

    render() {
        if( this.state.updateState  == true ){
            this.state.updateState  = false
        }else{
            this.getdata( this.props.code )
        }
        this.updateKchart()
        return (
            <div id="k_form" style={{ width: 1024, height: 700 }}></div>
        );
    }
}

MyKchart2.defaultProps = {
    code: 'RU0'
  }

export default MyKchart2;