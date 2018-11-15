import React from "react";
import {
  G2,
  Chart,
  Geom,
  Axis,
  Tooltip,
  Coord,
  Label,
  Legend,
  View,
  Guide,
  Shape,
  Facet,
  Util
} from "bizcharts";
import DataSet from "@antv/data-set";
import Slider from "bizcharts-plugin-slider";
import request from '../utils/request'

import dataObj from "./mock.json";
let data1 = dataObj.data;

// let data =  
//     [
//      { "time": "2015-04-07",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 },
//      { "time": "2015-04-08",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 },
//      { "time": "2015-04-09",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 },
//      { "time": "2015-04-10",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 },
//      { "time": "2015-04-11",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 },
//      { "time": "2015-04-12",  "volumn":100,"start":10.0,"end":15.0,"min":9.5,"max":16.0 } 

//    ]

//console.log('data:', data )


function getComponent(data) {
  
  const { DataView } = DataSet;
  const cols = {
    date: {
      type: "timeCat",
      nice: false,
      range: [0, 1]
    },
    trend: {
      values: ["上涨", "下跌"]
    },
    vol: {
      alias: "成交量"
    },
    open: {
      alias: "开盘价"
    },
    close: {
      alias: "收盘价"
    },
    high: {
      alias: "最高价"
    },
    low: {
      alias: "最低价"
    },
    range: {
      alias: "股票价格"
    }
  };
  // 设置状态量，时间格式建议转换为时间戳，转换为时间戳时请注意区间
  const ds = new DataSet({
    state: {
      start: "2018-09-01",
      end: "2018-11-15"
    }
  });
  const dv = ds.createView();
  dv.source(data)
    .transform({
      type: "filter",
      callback: obj => {
        const date = obj.date;
        return date <= ds.state.end && date >= ds.state.start;
      }
    })
    .transform({
      type: "map",
      callback: obj => {
        obj.trend = obj.open <= obj.close ? "上涨" : "下跌";
        obj.range = [obj.open, obj.close, obj.high, obj.low];
        return obj;
      }
    });

  class SliderChart extends React.Component {
    onChange(obj) {
      const { startText, endText } = obj;
      ds.setState("start", startText);
      ds.setState("end", endText);
    }

    render() {
      return (
        <div>
          <Chart
            width={1000} height={800} 
            // height={window.innerHeight - 50}
            animate={false}
            padding={[10, 40, 40, 40]}
            data={dv}
            scale={cols}
            forceFit
          >
            <Legend offset={20} />
            <Tooltip
              showTitle={false}
              itemTpl="<li data-index={index}><span style=&quot;background-color:{color};&quot; class=&quot;g2-tooltip-marker&quot;></span>{name}{value}</li>"
            />
            <View
              end={{
                x: 1,
                y: 0.5
              }}
              data={dv}
            >
              <Axis name="date" />
              <Axis name="range" />
              <Geom
                type="schema"
                position="time*range"
                color={[
                  "trend",
                  val => {
                    if (val === "上涨") {
                      return "#f04864";
                    }

                    if (val === "下跌") {
                      return "#2fc25b";
                    }
                  }
                ]}
                tooltip={[
                  "date*open*close*high*low",
                  (date, open, close, high, low) => {
                    return {
                      name: date,
                      value:
                        '<br><span style="padding-left: 16px">开盘价：' +
                        open +
                        "</span><br/>" +
                        '<span style="padding-left: 16px">收盘价：' +
                        close +
                        "</span><br/>" +
                        '<span style="padding-left: 16px">最高价：' +
                        high +
                        "</span><br/>" +
                        '<span style="padding-left: 16px">最低价：' +
                        low +
                        "</span>"
                    };
                  }
                ]}
                shape="candle"
              />
            </View>
            <View
              open={{
                x: 0,
                y: 0.65
              }}
              data={dv}
              scale={{
                volumn: {
                  tickCount: 2
                }
              }}
            >
              <Axis
                name="vol"
                label={{
                  formatter: function(val) {
                    return parseInt(val / 1000, 10) + "k";
                  }
                }}
              />
              <Axis name="date" tickLine={null} label={null} />
              <Geom
                type="interval"
                position="date*vol"
                color={[
                  "trend",
                  val => {
                    if (val === "上涨") {
                      return "#f04864";
                    }

                    if (val === "下跌") {
                      return "#2fc25b";
                    }
                  }
                ]}
                tooltip={[
                  "date*vol",
                  (date, vol) => {
                    return {
                      name: date,
                      value:
                        '<br/><span style="padding-left: 16px">成交量：' +
                        vol +
                        "</span><br/>"
                    };
                  }
                ]}
                shape="candle"
              />
            </View>
          </Chart>
          <div>
            <Slider
              padding={[20, 40, 20, 40]}
              width="auto"
              height={26}
              start={ds.state.start}
              end={ds.state.end}
              xAxis="date"
              yAxis="vol"
              scales={{
                date: {
                  type: "timeCat",
                  nice: false
                }
              }}
              data={data}
              onChange={this.onChange.bind(this)}
            />
          </div>
        </div>
      );
    }
  }
  return SliderChart;
}

class MyKchart extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date(), datalist:[] };
  }

  componentDidMount() {
      console.log( "MyKchart DidMount " )
      this.getdata( this.props.code )
      //this.setState({ datalist: this.state.datalist } ); 
  }

  getdata = ( code )=>{
    let dataUrl = '/future/kline/' + this.props.code 
    console.log( dataUrl )    
    request( dataUrl ).then(data => { 
      console.log('request : '+ dataUrl  +'  '+ this.props.code )
      if( data.data ){  
        
          let adata = data.data.data 
          console.log('request : ' + adata.length   )
          //console.log( adata[0] )
          this.state.datalist = adata
          // var   gettype=Object.prototype.toString;
          // console.log("type:", gettype.call(  adata )   )
          this.setState({ datalist: adata } );   
      }             
    })
} 


  render() {
    console.log( 'MyKchart render ', this.props.code )
    //this.getdata( this.props.code )

    let data = [ ];
    if( this.state.datalist ){
        data = this.state.datalist ;  
        // data.forEach( (rec,index,arr)=>{
        //   rec.zf = rec.zf.toFixed(2)
         
        // } )
    }    
    console.log('data:', data)
    const SliderChart = getComponent(data);
    return (
      <div>
        <SliderChart />
      </div>
    );
  }
}

MyKchart.defaultProps = {
  code: 'RU0'
}

export default MyKchart;
